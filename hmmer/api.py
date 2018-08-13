from rest_framework import viewsets
from app.models import Organism
from hmmer.models import HmmerDB, HmmerQueryRecord
from hmmer.serializers import OrganismSerializer, HmmerDbSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser

class OrganismViewSet(viewsets.ModelViewSet):
    """
    Retrieve organisms.
    """
    queryset = Organism.objects.all()
    serializer_class = OrganismSerializer
    lookup_field = 'short_name'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)


class HmmerDbViewSet(viewsets.ModelViewSet):
    """
    Retrieve Hmmer databases.
    """
    queryset = HmmerDB.objects.all()
    serializer_class = HmmerDbSerializer
    lookup_field = 'title'
    lookup_value_regex = '[^/]+'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,)

