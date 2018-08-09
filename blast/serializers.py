from rest_framework.serializers import HyperlinkedModelSerializer, ReadOnlyField, HyperlinkedRelatedField
from app.models import Organism
from blast.models import SequenceType, BlastDb


class OrganismSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Organism
        fields = ('display_name', 'short_name', 'description', 'tax_id')


class SequenceTypeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = SequenceType
        fields = ('molecule_type', 'dataset_type')


class BlastDbSerializer(HyperlinkedModelSerializer):
    organism = HyperlinkedRelatedField(
        view_name='blast:organism-detail',
        lookup_field='short_name',
        read_only=True)
    type = HyperlinkedRelatedField(
        view_name='blast:sequencetype-detail',
        lookup_field='dataset_type',
        read_only=True)
    fasta_file_exists = ReadOnlyField()
    blast_db_files_exists = ReadOnlyField()
    sequence_set_exists = ReadOnlyField()
    db_ready = ReadOnlyField()

    class Meta:
        model = BlastDb
        fields = ('organism', 'type', 'fasta_file', 'title', 'description',
                  'is_shown', 'fasta_file_exists', 'blast_db_files_exists',
                  'sequence_set_exists', 'db_ready')
