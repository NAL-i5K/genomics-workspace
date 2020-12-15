from django.conf.urls import url
from hmmer import views
# from .api import *
from django.urls import path, re_path

app_name='hmmer'
urlpatterns = [
    # ex: /hmmer/
    re_path(r'^$', views.create, name='create'),
    # ex: /hmmer/task/5/
    re_path(r'^task/(?P<task_id>[0-9a-zA-Z]+)$', views.retrieve, name='retrieve'),
    re_path(r'^task/(?P<task_id>[0-9a-zA-Z]+)/status$', views.status, name='status'),
    # url(r'^api/', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-docs/', include('rest_framework_swagger.urls')),
    re_path('^user-tasks/(?P<user_id>[0-9]+)$', views.user_tasks),
    re_path(r'^manual/$', views.manual, name='manual'),
]
