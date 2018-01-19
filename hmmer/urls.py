from django.conf.urls import url
from hmmer import views

urlpatterns = [
    # ex: /blast/
    url(r'^$', views.create, name='create'),
    # url(r'^iframe$', views.create, {'iframe': True}, name='iframe'),
    # ex: /blast/5/
    url(r'^(?P<task_id>[0-9a-zA-Z]+)$', views.retrieve, name='retrieve'),
    url(r'^(?P<task_id>[0-9a-zA-Z]+)/status$', views.status, name='status'),
    url('manual/', views.manual, name='manual'),
]
