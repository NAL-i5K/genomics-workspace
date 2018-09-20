from django.conf.urls import url, include
from django.conf import settings
from blast import views
from blast.api import OrganismViewSet, SequenceTypeViewSet, BlastDbViewSet, SequenceViewSet, BlastQueryRecordViewSet, UserViewSet
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
    # url(r'^iframe$', views.create, {'iframe': True}, name='iframe'),
    # ex: /blast/5/
    url(r'^task/(?P<task_id>[0-9a-zA-Z]+)$', views.retrieve, name='retrieve'),
    url(r'^task/(?P<task_id>[0-9a-zA-Z]+)/status$', views.status, name='status'),
    # url(r'^read_gff3/(?P<task_id>[0-9a-fA-F]*)/*(?P<dbname>[\w\-\|.]*)/*$', views.read_gff3, name='read_gff3'),
    url(r'^api/', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-docs/', include('rest_framework_swagger.urls')),
    url(r'^user-tasks/(?P<user_id>[0-9]+)$', views.user_tasks),
    url(r'^manual/$', views.manual, name='manual'),
]

if settings.DEBUG:
    from blast import test_views
    urlpatterns += [
        url(r'^test/$', test_views.test_main)
    ]
