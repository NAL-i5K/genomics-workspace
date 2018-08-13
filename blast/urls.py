from blast import views
from blast.api import OrganismViewSet, SequenceTypeViewSet, BlastDbViewSet
from django.conf.urls import url, include
from django.conf import settings
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'organism', OrganismViewSet)
router.register(r'seqtype', SequenceTypeViewSet)
router.register(r'blastdb', BlastDbViewSet)

urlpatterns = [
    # ex: /blast/
    url(r'^$', views.create, name='create'),
    # url(r'^iframe$', views.create, {'iframe': True}, name='iframe'),
    # ex: /blast/5/
    url(r'^task/(?P<task_id>[0-9a-zA-Z]+)$', views.retrieve, name='retrieve'),
    url(r'^task/(?P<task_id>[0-9a-zA-Z]+)/status$',
        views.status,
        name='status'),
    # url(r'^read_gff3/(?P<task_id>[0-9a-fA-F]*)/*(?P<dbname>[\w\-\|.]*)/*$', views.read_gff3, name='read_gff3'),
    url(r'^api/seq/(?P<seq_id>[a-zA-Z0-9_-]+)/', views.get_seq, name='seq'),
    url(r'^api/', include(router.urls)),
]

if settings.DEBUG:
    from blast import test_views
    urlpatterns += [url(r'^test/$', test_views.test_main)]
