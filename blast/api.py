from rest_framework import renderers, viewsets
from app.models import Organism
from blast.models import SequenceType, BlastDb
from blast.serializers import OrganismSerializer, BlastDbSerializer, SequenceTypeSerializer

class OrganismViewSet(viewsets.ModelViewSet):
    """
    Retrieve organisms.
    """
    queryset = Organism.objects.all()
    serializer_class = OrganismSerializer
    lookup_field = 'short_name'


class SequenceTypeViewSet(viewsets.ModelViewSet):
    """
    Retrieve sequence types.
    """
    queryset = SequenceType.objects.all()
    serializer_class = SequenceTypeSerializer
    lookup_field = 'dataset_type'


class BlastDbViewSet(viewsets.ModelViewSet):
    """
    Retrieve BLAST databases.
    """
    queryset = BlastDb.objects.all()
    serializer_class = BlastDbSerializer
    lookup_field = 'title'
    lookup_value_regex = '[^/]+'
