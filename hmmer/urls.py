from django.conf.urls import url, include
from hmmer import views
from hmmer.api import HmmerDbViewSet, OrganismViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'organism', OrganismViewSet)
router.register(r'hmmerdb', HmmerDbViewSet)

urlpatterns = [
    # ex: /hmmer/
    url(r'^$', views.create, name='create'),
    # ex: /hmmer/task/5/
    url(r'^task/(?P<task_id>[0-9a-zA-Z]+)$', views.retrieve, name='retrieve'),
    url(r'^task/(?P<task_id>[0-9a-zA-Z]+)/status$',
        views.status,
        name='status'),
    url(r'^manual/$', views.manual, name='manual'),
    url(r'^api/', include(router.urls)),
]
