from datetime import datetime
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, password_reset, password_reset_done, password_reset_complete, password_change_done, password_reset_confirm
from django.contrib.auth.decorators import user_passes_test
from app.forms import BootstrapAuthenticationForm, BootStrapPasswordChangeForm, BootStrapPasswordResetForm, BootStrapSetPasswordForm
from app.views import about, set_institution, info_change, register, logout_all, password_change

admin.autodiscover()
# admin.site.unregister(Site)
# from filebrowser.sites import site

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/home')

urlpatterns = [
    url(r'^about', about, name='about'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    # url(r'^grappelli/', include('grappelli.urls')),
    # Enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls'), name='doc'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^proxy/', include('proxy.urls', namespace='proxy')),

    # user authentication
    url(r'^set_institution$', set_institution, name='set_institution'),
    url(r'^info_change$', info_change, name='info_change'),
    url(r'^register$', register, name='register'),
    url(r'^login/$', login_forbidden(login),
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
    url(r'^logout$', logout_all, name='logout'),
    url(r'^password_reset$', password_reset,
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
    url(r'^password_reset_done$', password_reset_done,
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
        password_reset_confirm,
        {
            'template_name': 'app/password_reset_confirm.html',
            'set_password_form': BootStrapSetPasswordForm,
            'extra_context':
            {
                'year': datetime.now().year,
            },
        },
        name='password_reset_confirm'),
    url(r'^reset_complete$', password_reset_complete,
        {
            'template_name': 'app/password_reset_complete.html',
            'extra_context':
            {
                'title': 'Password reset complete',
                'year': datetime.now().year,
            },
        },
        name='password_reset_complete'),
    url(r'^password_change_done$', password_change_done,
        {
            'template_name': 'app/password_change_done.html',
            'extra_context':
            {
                'title': 'Password changed',
                'year': datetime.now().year,
            },
        },
        name='password_change_done'),
    url(r'^password_change$', password_change,
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

    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # BLAST
    url(r'^blast/', include('blast.urls', namespace='blast')),
    # HMMER
    url(r'^hmmer/', include('hmmer.urls', namespace='hmmer')),
    # CLUSTAL
    url(r'^clustal/', include('clustal.urls', namespace='clustal')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
