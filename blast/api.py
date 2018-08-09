from rest_framework import renderers, viewsets
from app.models import Organism
from blast.models import SequenceType, BlastDb
from blast.serializers import OrganismSerializer, BlastDbSerializer, SequenceTypeSerializer


class FASTARenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'fasta'

    def render(self, data, media_type=None, renderer_context=None):
        if 'results' in data:
            return ''.join([seq['fasta_seq'] for seq in data['results']])
        elif 'fasta_seq' in data:
            return data['fasta_seq']
        else:
            return ''


class OrganismViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve organisms.
    """
    queryset = Organism.objects.all()
    serializer_class = OrganismSerializer
    lookup_field = 'short_name'


class SequenceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve sequence types.
    """
    queryset = SequenceType.objects.all()
    serializer_class = SequenceTypeSerializer
    lookup_field = 'dataset_type'


class BlastDbViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve BLAST databases.
    """
    queryset = BlastDb.objects.all()
    serializer_class = BlastDbSerializer
    lookup_field = 'title'
    lookup_value_regex = '[^/]+'
