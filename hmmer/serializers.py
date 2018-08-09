from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, HyperlinkedIdentityField, ReadOnlyField, HyperlinkedRelatedField
from django.contrib.auth.models import User
from app.models import Organism
from hmmer.models import HmmerDB, HmmerQueryRecord


class OrganismSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Organism
        fields = ('display_name', 'short_name', 'description', 'tax_id')


class HmmerDbSerializer(HyperlinkedModelSerializer):
    organism = HyperlinkedRelatedField(
        view_name='hmmer:organism-detail',
        lookup_field='short_name',
        read_only=True)

    class Meta:
        model = HmmerDB
        fields = ('organism', 'fasta_file', 'title', 'description', 'is_shown')
