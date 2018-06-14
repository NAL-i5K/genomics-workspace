from datetime import datetime
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from app.views import about

admin.autodiscover()
# admin.site.unregister(Site)
# from filebrowser.sites import site

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/home')

urlpatterns = [
    url(r'^about', about, name='about'),

    url(r'^proxy/', include('proxy.urls', namespace='proxy')),

    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls'), name='doc'),
    url(r'^admin/filebrowser/', include('filebrowser.urls')),

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
