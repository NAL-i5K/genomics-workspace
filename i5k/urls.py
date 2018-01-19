from datetime import datetime
from django.conf import settings
from django.conf.urls import include, url
from app.forms import BootstrapAuthenticationForm, BootStrapPasswordChangeForm, BootStrapPasswordResetForm, BootStrapSetPasswordForm
from django.contrib import admin
from django.contrib.auth.views import login
from django.contrib.auth.decorators import user_passes_test

admin.autodiscover()

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/home')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls'), name='doc'),
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^blast/', include('blast.urls', namespace='blast')),
    url(r'^hmmer/', include('hmmer.urls', namespace='hmmer')),
    url(r'^clustal/', include('clustal.urls', namespace='clustal')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    ]
