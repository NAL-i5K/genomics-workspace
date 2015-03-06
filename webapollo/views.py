# coding: utf-8
import requests, json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Permission
from django.core.cache import cache
from .models import Species, SpeciesPassword, Registration, insert_species_permission, delete_species_permission
from userprofile.models import Profile


@csrf_exempt
@staff_member_required
def manage(request):
    if request.method == 'GET':
        pendings = Registration.objects.filter(status='Pending').order_by('submission_time')
        #users = User.objects.all()
        profiles = Profile.objects.select_related('user').all()
        users = []
        for p in profiles:
            users.append({
                'id': p.id,
                'full_name': p.user.first_name + ' ' + p.user.last_name,
                'username': p.user.username,
                'institution': p.institution,
            })
           
    return render(
        request,
        'webapollo/manage.html', {
            'pendings': pendings,
            'users': users,
        }
    )


@csrf_exempt
@staff_member_required
def user_permission(request, user_id):
    if request.method == 'GET':
        profile = Profile.objects.select_related('user').get(pk=user_id)
        user = {
            'full_name': profile.user.first_name + ' ' + profile.user.last_name,
            'username': profile.user.username,
            'institution': profile.institution,
        }
        
        species = Species.objects.all()
        species_list = []
        for s in species:
            perms = profile.user.user_permissions.filter(codename__startswith=s.name)
            perm_values = {'read': False, 'write': False, 'publish': False, 'admin': False, 'owner': False}
            for perm in perms:
                perm_name = perm.name.split('_',2)[1]
                perm_values[perm_name] = True
                        
            species_list.append({
                'name': s.name,
                'full_name': s.full_name,
                'perm_values': perm_values
            })

    return render(
        request,
        'webapollo/user_permission.html', {
            'user': user,
            'species_list': species_list,
        }
    )


@login_required
def species(request, species_name):
    if not request.user.user_permissions.filter(codename__startswith=species_name):
        return HttpResponse('You do not have permissions to access the instance.')

    species = Species.objects.get(name=species_name)
    response = HttpResponseRedirect(species.url)
    login_url = species.url + '/Login?operation=login'
    
    spe_pwd = SpeciesPassword.objects.get(user=request.user, species=species)
    user = { 'username': request.user.username, 'password': spe_pwd.pwd }

    # store cookie value (ex. JSESSION=08D90CDE33092788F7462A969D2C398E) in memcached
    # to avoid multiple sessions when logging in WebApollo
    cache_id = request.user.username + '_' + species_name + '_cookie' # an unique cache id
    if cache.get(cache_id) is None:
        with requests.Session() as s:
            s.post(login_url, json.dumps(user))
            for cookie in s.cookies:
                if cookie.name == 'JSESSIONID':
                    response.set_cookie(cookie.name, value=cookie.value, domain='.nal.usda.gov', path='/' + species_name + '/')
                    cache.set( cache_id, {cookie.name: cookie.value}, 1800 ) # timeout = 30 mins
    else:
        k, v = cache.get(cache_id).items()[0] # always only one dict in the cache
        response.set_cookie(k, value=v, domain='.nal.usda.gov', path='/' + species_name + '/')
                
    return response
