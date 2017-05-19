from datetime import datetime
from django.conf.urls import patterns, include, url
from app.forms import BootstrapAuthenticationForm, BootStrapPasswordChangeForm, BootStrapPasswordResetForm, BootStrapSetPasswordForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.views import login
from django.contrib.auth.decorators import user_passes_test

admin.autodiscover()
#admin.site.unregister(Site)
#from filebrowser.sites import site

login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/home')

urlpatterns = patterns('',

    url(r'^tripal_assembly_data', 'app.views.tripal_assembly_data', name='tripal_assembly_data'),
    url(r'^tripal_gene_prediction', 'app.views.tripal_gene_prediction', name='tripal_gene_prediction'),
    url(r'^tripal_mapped', 'app.views.tripal_mapped', name='tripal_mapped'),
    url(r'^web_login$', 'app.views.web_login', name='web_login'),
    url(r'^web_logout$', 'app.views.web_logout', name='web_logout'),
    url(r'^home$', 'dashboard.views.dashboard', name='dashboard'),
    url(r'^dashboard$', 'dashboard.views.dashboard', name='dashboard'),
    url(r'blast_hist', 'dashboard.views.dashboard', name='dashboard'),
    url(r'clustal_hist', 'dashboard.views.dashboard', name='dashboard'),
    #url(r'^home/', include('dashboard.urls', namespace='dashboard')),
    #url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^about', 'app.views.about', name='about'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    #url(r'^admin/filebrowser/', include(site.urls)),
    #url(r'^grappelli/', include('grappelli.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls'), name='doc'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^proxy/', include('proxy.urls', namespace='proxy')),
    #url(r'^webapollo/', include('webapollo.urls', namespace='webapollo')),

    # user authentication
    url(r'^set_institution$', 'app.views.set_institution', name='set_institution'),
    url(r'^info_change$', 'app.views.info_change', name='info_change'),
    url(r'^register$', 'app.views.register', name='register'),
    url(r'^login/$',
        #'django.contrib.auth.views.logini',
        login_forbidden(login),
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            },
        },
        name='login'),
    url(r'^logout$', 'app.views.logout_all', name='logout'),
    url(r'^password_reset$',
        'django.contrib.auth.views.password_reset',
        {
            'template_name': 'app/password_reset.html',
            'password_reset_form': BootStrapPasswordResetForm,
            'extra_context':
            {
                'title': 'Password reset',
                'year': datetime.now().year,
            },
        },
        name='password_reset'),
    url(r'^password_reset_done$',
        'django.contrib.auth.views.password_reset_done',
        {
            'template_name': 'app/password_reset_done.html',
            'extra_context':
            {
                'title': 'Password reset sent',
                'year': datetime.now().year,
            },
        },
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        #'django.contrib.auth.views.password_reset_confirm',
        'app.views.testView',
        {
            'template_name': 'app/password_reset_confirm.html',
            'set_password_form': BootStrapSetPasswordForm,
            'extra_context':
            {
                'year': datetime.now().year,
            },
        },
        name='password_reset_confirm'),
    url(r'^reset_complete$',
        'django.contrib.auth.views.password_reset_complete',
        {
            'template_name': 'app/password_reset_complete.html',
            'extra_context':
            {
                'title': 'Password reset complete',
                'year': datetime.now().year,
            },
        },
        name='password_reset_complete'),
    url(r'^password_change_done$',
        'django.contrib.auth.views.password_change_done',
        {
            'template_name': 'app/password_change_done.html',
            'extra_context':
            {
                'title': 'Password changed',
                'year': datetime.now().year,
            },
        },
        name='password_change_done'),
    url(r'^password_change$',
        #'django.contrib.auth.views.password_change',
        'app.views.password_change',
        {
            'template_name': 'app/password_change.html',
            'password_change_form': BootStrapPasswordChangeForm,
            'post_change_redirect': 'password_change_done',
            'extra_context':
            {
                'title': 'Change password',
                'year': datetime.now().year,
            },
        },
        name='password_change'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # BLAST
    url(r'^blast/', include('blast.urls', namespace='blast')),
    # BLAST
    #url(r'^data/', include('data.urls', namespace='data')),

    url(r'^hmmer/', include('hmmer.urls', namespace='hmmer')),
    url(r'^clustal/', include('clustal.urls', namespace='clustal')),
    url(r'^sso/', include('webapollo_sso.urls', namespace='sso')),
)
from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
