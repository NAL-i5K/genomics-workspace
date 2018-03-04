import requests
import json
from datetime import datetime
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.views import logout, password_reset_confirm
from django.contrib.contenttypes.models import ContentType
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


def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html', {
            'title': 'Home Page',
            #'year': datetime.now().year,
        })

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html', {
            'title': 'Contact',
            'message': 'National Agricultural Library',
            #'year': datetime.now().year,
        })

def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html', {
            'title': 'About i5k - BLAST',
            'message': 'django-blast',
            #'year': datetime.now().year,
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
            'year': datetime.now().year,
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
            'year': datetime.now().year,
            'title': 'Update Account Info',
            'form': form,
            'msg': msg,
            'isOAuth': isOAuth,
            'errors': errors,
        })
    except:
        return HttpResponseRedirect(reverse('set_institution'))

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