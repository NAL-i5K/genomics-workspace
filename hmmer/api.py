from rest_framework import viewsets
from app.models import Organism
from hmmer.models import HmmerDB, HmmerQueryRecord
from hmmer.serializers import OrganismSerializer, HmmerDbSerializer


class OrganismViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve organisms.
    """
    queryset = Organism.objects.all()
    serializer_class = OrganismSerializer
    lookup_field = 'short_name'


class HmmerDbViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve Hmmer databases.
    """
    queryset = HmmerDB.objects.all()
    serializer_class = HmmerDbSerializer
    lookup_field = 'title'
    lookup_value_regex = '[^/]+'
