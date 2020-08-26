from django.conf.urls import url
from clustal import views
# from .api import *
from django.urls import path, re_path

app_name='clustal'
urlpatterns = [
    # ex: /clustal/
    re_path(r'^$', views.create, name='create'),
    # ex: /clustal/5/
    re_path(r'^task/(?P<task_id>[0-9a-zA-Z]+)$', views.retrieve, name='retrieve'),
    re_path(r'^task/(?P<task_id>[0-9a-zA-Z]+)/status$', views.status, name='status'),
    # re_path(r'^api/', include(router.urls)),
    # re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # re_path(r'^api-docs/', include('rest_framework_swagger.urls')),
    re_path(r'^user-tasks/(?P<user_id>[0-9]+)$', views.user_tasks),
    re_path(r'^manual/$', views.manual, name='manual'),
]
