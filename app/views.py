import requests
import json
from datetime import datetime
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.conf import settings
from django.utils.http import is_safe_url
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME, login, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.views import logout, password_reset_confirm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.apps import apps
from functools import wraps
from .forms import InfoChangeForm, SetInstitutionForm, RegistrationForm
from .models import Profile
from social.apps.django_app.default.models import UserSocialAuth
from i5k.settings import DRUPAL_URL, DRUPAL_COOKIE_DOMAIN
from drupal_sso.models import DrupalUserMapping
from webapollo_sso.models import PermsRequest, UserMapping
from django.contrib.auth.models import User
from Crypto.Cipher import AES
import base64
import i5k.settings
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
import urllib2
import cookielib


def _tripal_login(tripal_login_url, user):

    def _get_url_request(url):
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        return req

    def _get_url_open():
        cookies = cookielib.LWPCookieJar()
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookies),
        ]
        opener = urllib2.build_opener(*handlers)
        return opener, cookies

    try:

        user_info = DrupalUserMapping.objects.get(django_user=user)
        password = user_info.drupal_user_pwd
        old_user = True

    except DrupalUserMapping.DoesNotExist:

        old_user = False
        password = User.objects.make_random_password(length=20)

    data = {"name" : user.username, "pass" : password}

    req = _get_url_request(tripal_login_url)
    opener, cookies = _get_url_open()

    try:

        response = opener.open(req, json.dumps(data))
        result = json.loads(response.read())
        if(old_user==False):
            DrupalUserMapping.objects.create(django_user=user, drupal_user_pwd=password)

    except:
        print "login fail"
        pass

    opener.close()

    return cookies

# tripal submit form
def tripal_assembly_data(request):

    print DRUPAL_URL + '/datasets/assembly-data'
    print request.user.username
    response = HttpResponseRedirect(DRUPAL_URL + '/datasets/assembly-data')
    cookies = _tripal_login(DRUPAL_URL + '/rest/user/login', request.user)

    for cookie in cookies:
        response.set_cookie(key=cookie.name, value=cookie.value, domain=DRUPAL_COOKIE_DOMAIN, path=cookie.path)

    return response

def tripal_gene_prediction(request):

    response = HttpResponseRedirect(DRUPAL_URL + '/datasets/gene-prediction')
    cookies = _tripal_login(DRUPAL_URL + '/rest/user/login', request.user)

    for cookie in cookies:
        response.set_cookie(key=cookie.name, value=cookie.value, domain=DRUPAL_COOKIE_DOMAIN, path=cookie.path)

    return response

def tripal_mapped(request):

    response = HttpResponseRedirect(DRUPAL_URL + '/datasets/mapped')
    cookies = _tripal_login(DRUPAL_URL + '/rest/user/login', request.user)

    for cookie in cookies:
        response.set_cookie(key=cookie.name, value=cookie.value, domain=DRUPAL_COOKIE_DOMAIN, path=cookie.path)

    return response

#weblogin/weblogout for tripal
def web_login(request):

        if request.user.is_authenticated() == True:
            return HttpResponse(json.dumps({'user':request.user.username, 'sessionid': request.session._session_key, 'email':request.user.email}), content_type="application/json")

        print request.COOKIES
        username = request.GET['username']
        password = request.GET['password']
        #username = userdata['username']
        #password = userdata['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            print request.session._session_key
            return HttpResponse(json.dumps({'user':request.user.username, 'sessionid': request.session._session_key, 'email':request.user.email}), content_type="application/json")
            #return HttpResponse(json.dumps({'sessionid': request.COOKIES['sessionid']}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'error':'login failed'}), content_type="application/json")

def web_logout(request):
    logout(request)
    return HttpResponse(json.dumps({}), content_type="application/json")

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html', {
            'title': 'Home Page',
        })

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html', {
            'title': 'Contact',
            'message': 'National Agricultural Library',
        })

def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html', {
            'title': 'About i5k - BLAST',
            'message': 'django-blast',
        })

def checkOAuth(_user):
    return UserSocialAuth.objects.filter(user=_user).exists()

def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        return HttpResponse(json.dumps({ 'invalid_request': True }), content_type='application/json')
    return wrapper

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        def _get_url_request(url):
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            return req

        def _get_url_open():
            cookies = cookielib.LWPCookieJar()
            handlers = [
                urllib2.HTTPHandler(),
                urllib2.HTTPSHandler(),
                urllib2.HTTPCookieProcessor(cookies)
                ]
            opener = urllib2.build_opener(*handlers)
            return opener

        if form.is_valid():
            new_user = form.save();
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])

            try:
                if new_user is not None:
                    data = {"firstName" : form.cleaned_data['first_name'], "lastName" : form.cleaned_data['last_name'],
                            "email": form.cleaned_data['username'], "newPassword" : form.cleaned_data['password1'], "role" : "USER"}
                    data.update({'username':i5k.settings.ROBOT_ID, 'password':i5k.settings.ROBOT_PWD})

                    req = _get_url_request(i5k.settings.APOLLO_URL+'/user/createUser')
                    opener = _get_url_open()
                    response = opener.open(req, json.dumps(data))
                    result = json.loads(response.read())

                    opener.close()


                    if(len(result) == 0):
                        data = {"userId": form.cleaned_data['username']}
                        data.update({'username':i5k.settings.ROBOT_ID, 'password':i5k.settings.ROBOT_PWD})

                        req = _get_url_request(i5k.settings.APOLLO_URL+'/user/loadUsers')
                        opener = _get_url_open()
                        response = opener.open(req, json.dumps(data))
                        users = json.loads(response.read())

                        for user in users:
                            if(user['username'] == form.cleaned_data['username']):
                                userId = user['userId']
                                break

                        user_info = UserMapping.objects.create(apollo_user_id=userId,
                                                               apollo_user_name=form.cleaned_data['username'],
                                                               apollo_user_pwd=encodeAES(form.cleaned_data['password1']),
                                                               django_user=User.objects.get(username=form.cleaned_data['username']))
                        user_info.save()

                        opener.close()

            except:
                print "apollo is down"
                pass

            login(request, new_user)
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = RegistrationForm()
    return render(request, "app/register.html", {
        'form': form,
        'title': 'Registration',
    })

@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
        template_name,
        post_change_redirect,
        password_change_form,
        current_app=None, extra_context=None):
    print 'aa'
    post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        print request.POST['new_password1']
        if form.is_valid():
            form.save()


            def _get_url_request(url):
                req = urllib2.Request(url)
                req.add_header('Content-Type', 'application/json')
                return req

            def _get_url_open():
                cookies = cookielib.LWPCookieJar()
                handlers = [
                    urllib2.HTTPHandler(),
                    urllib2.HTTPSHandler(),
                    urllib2.HTTPCookieProcessor(cookies)
                    ]
                opener = urllib2.build_opener(*handlers)
                return opener

            try:
                new_password = request.POST['new_password1']

                user_info = UserMapping.objects.get(django_user=request.user)
                userId = user_info.apollo_user_id

                opener = _get_url_open()
                response = opener.open(_get_url_request(i5k.settings.APOLLO_URL+'/Login?operation=login'),
                                   json.dumps({'username':i5k.settings.ROBOT_ID, 'password':i5k.settings.ROBOT_PWD}))
                result = json.loads(response.read())

                req = _get_url_request(i5k.settings.APOLLO_URL+'/user/loadUsers')
                response = opener.open(req, json.dumps({"userId" : userId}))
                users = json.loads(response.read())

                firstName = users[0]['firstName']
                lastName  = users[0]['lastName']
                username  = users[0]['username']
                role      = users[0]['role']

                opener.close()

                data = {"userId" : userId, "newPassword": new_password, "role": role, "firstName": firstName, 'lastName': lastName, 'email': username}
                data.update({'username':i5k.settings.ROBOT_ID, 'password':i5k.settings.ROBOT_PWD})

                req = _get_url_request(i5k.settings.APOLLO_URL+'/user/updateUser')
                opener = _get_url_open()
                response = opener.open(req, json.dumps(data))
                result = json.loads(response.read())

                if(len(result)==0):
                    user_info.apollo_user_pwd = encodeAES(new_password)
                    user_info.save()

                opener.close()

            except:
                print "apollo is down"
                opener.close()

            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': 'Password change',
    }
    if extra_context is not None:
        context.update(extra_context)
    context.update({'isOAuth': checkOAuth(request.user)})
    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@login_required
def set_institution(request):
    if request.method == 'POST':
        form = SetInstitutionForm(request.POST)
        if form.is_valid():
            p = Profile()
            p.user = request.user
            p.institution = form.cleaned_data['institution']
            p.save()
    else:
        form = SetInstitutionForm()

    try:
        p = Profile.objects.get(user=request.user)
        return HttpResponseRedirect(reverse('dashboard'))
    except ObjectDoesNotExist:
        return render(
            request,
            'app/set_institution.html', {
            'title': 'Specify your institution',
            'form': form,
        })

@login_required
def info_change(request):
    isOAuth = checkOAuth(request.user)
    try:
        p = Profile.objects.select_related('user').get(user=request.user)
        msg = ''
        errors = []
        if request.method == 'POST':
            if isOAuth:
                form = SetInstitutionForm(request.POST, instance=p)
            else:
                form = InfoChangeForm(request.POST, instance=p)
            if form.is_valid():
                form.save()
                if isOAuth:
                    msg = 'Your institution was updated.'
                else:
                    msg = 'Your account info was updated.'
            else:
                errors = str(form.errors)
        form = InfoChangeForm(instance=p)
        return render(
            request,
            'app/info_change.html', {
            'title': 'Update Account Info',
            'form': form,
            'msg': msg,
            'isOAuth': isOAuth,
            'errors': errors,
        })
    except:
        return HttpResponseRedirect(reverse('set_institution'))

# customized version of django.contrib.auth.views.login function
@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_all(request, template_name='registration/login.html',
              redirect_field_name=REDIRECT_FIELD_NAME,
              authentication_form=AuthenticationForm,
              current_app=None, extra_context=None):
    if request.user.is_authenticated():
        return redirect('dashboard')
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))
    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
       context.update(extra_context)

    if current_app is not None:
       request.current_app = current_app
    
    return TemplateResponse(request, template_name, context)

@login_required
def logout_all(request):
    if apps.is_installed('webapollo'):
        from webapollo.views import logout_all_instances
        logout_all_instances(request)
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def encodeAES(password):
    BLOCK_SIZE = 32
    PADDING = '{'
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    cipher = AES.new(i5k.settings.SSO_CIPHER)
    encoded = base64.b64encode(cipher.encrypt(pad(password)))
    return encoded

def decodeAES(encoded):
    PADDING = '{'
    cipher = AES.new(i5k.settings.SSO_CIPHER)
    decoded  = cipher.decrypt(base64.b64decode(encoded)).rstrip(PADDING)
    return decoded

def testView(request, uidb64, token, template_name, set_password_form, post_reset_redirect=None, extra_context=None):
    httpresponse = password_reset_confirm(request, uidb64=uidb64, token=token, template_name=template_name, set_password_form=set_password_form, extra_context=extra_context)
    if type(httpresponse) == HttpResponseRedirect:

        def _get_url_request(url):
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            return req

        def _get_url_open():
            cookies = cookielib.LWPCookieJar()
            handlers = [
                urllib2.HTTPHandler(),
                urllib2.HTTPSHandler(),
                urllib2.HTTPCookieProcessor(cookies)
                ]
            opener = urllib2.build_opener(*handlers)
            return opener

        #copy from password_reset_confirm

        UserModel = get_user_model()
        assert uidb64 is not None and token is not None
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserModel._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        try:
	    new_password = request.POST['new_password1']
	    user_info = UserMapping.objects.get(django_user=user)
	    userId = user_info.apollo_user_id

	    opener = _get_url_open()
	    response = opener.open(_get_url_request(i5k.settings.APOLLO_URL+'/Login?operation=login'),
					   json.dumps({'username':i5k.settings.ROBOT_ID, 'password':i5k.settings.ROBOT_PWD}))
	    result = json.loads(response.read())

	    req = _get_url_request(i5k.settings.APOLLO_URL+'/user/loadUsers')
	    response = opener.open(req, json.dumps({"userId" : userId}))
	    users = json.loads(response.read())

	    firstName = users[0]['firstName']
	    lastName  = users[0]['lastName']
	    username  = users[0]['username']
	    role      = users[0]['role']

	    opener.close()

	    data = {"userId" : userId, "newPassword": new_password, "role": role, "firstName": firstName, 'lastName': lastName, 'email': username}
	    data.update({'username':i5k.settings.ROBOT_ID, 'password':i5k.settings.ROBOT_PWD})

	    req = _get_url_request(i5k.settings.APOLLO_URL+'/user/updateUser')
	    opener = _get_url_open()
	    response = opener.open(req, json.dumps(data))
	    result = json.loads(response.read())

	    if(len(result)==0):
                user_info.apollo_user_pwd = encodeAES(new_password)
		user_info.save()

            opener.close()
        except:
            opener.close()
            pass

    return httpresponse


