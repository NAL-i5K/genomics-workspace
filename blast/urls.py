from __future__ import absolute_import
from django.conf.urls import url, include
from django.conf import settings
from blast import views
from blast.api import (OrganismViewSet, SequenceTypeViewSet, BlastDbViewSet,
                       SequenceViewSet, BlastQueryRecordViewSet, UserViewSet)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'organism', OrganismViewSet)
router.register(r'seqtype', SequenceTypeViewSet)
router.register(r'blastdb', BlastDbViewSet)
router.register(r'seq', SequenceViewSet)
router.register(r'task', BlastQueryRecordViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    # ex: /blast/
    url(r'^$', views.create, name='create'),
    # ex: /blast/5/
    url(r'^(?P<task_id>[0-9a-zA-Z]+)$', views.retrieve, name='retrieve'),
    url(r'^(?P<task_id>[0-9a-zA-Z]+)/status$', views.status, name='status'),
    url(r'^api/', include(router.urls)),
]

if settings.DEBUG:
    from blast import test_views
    urlpatterns += [
        url(r'^test/$', test_views.test_main)
    ]
