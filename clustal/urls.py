from django.conf.urls import url
from clustal import views

urlpatterns = [
    # ex: /clustal/
    url(r'^$', views.create, name='create'),
    # ex: /clustal/5/
    url(r'^task/(?P<task_id>[0-9a-zA-Z]+)$', views.retrieve, name='retrieve'),
    url(r'^task/(?P<task_id>[0-9a-zA-Z]+)/status$',
        views.status,
        name='status'),
    url(r'^manual/$', views.manual, name='manual'),
]
