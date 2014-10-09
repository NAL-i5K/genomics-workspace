from rest_framework import serializers
from .models import Sequence

class SequenceSerializer(serializers.ModelSerializer):
    fasta_seq = serializers.Field()

    class Meta:
        model = Sequence
        fields = ('blast_db', 'id', 'length', 'seq_start_pos', 'seq_end_pos', 'modified_date', 'fasta_seq', )