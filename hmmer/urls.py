from django.conf.urls import url
from hmmer import views
# from .api import *

urlpatterns = [
    # ex: /hmmer/
    url(r'^$', views.create, name='create'),
    # ex: /hmmer/task/5/
    url(r'^task/(?P<task_id>[0-9a-zA-Z]+)$', views.retrieve, name='retrieve'),
    url(r'^task/(?P<task_id>[0-9a-zA-Z]+)/status$', views.status, name='status'),
    # url(r'^api/', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^user-tasks/(?P<user_id>[0-9]+)$', views.user_tasks),
    url(r'^manual/$', views.manual, name='manual'),
]
