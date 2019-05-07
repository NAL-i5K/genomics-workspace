from blast.models import BlastDb,SequenceType,Sequence
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from app.models import Organism
import sys
import os
import django.db
from filebrowser.fields import FileBrowseField
class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('BlastDb', nargs='+', type=str, help='enter the blastdb name')

    def handle(*args,**options):
        title = options['BlastDb'][0]
        blast = BlastDb.objects.get(title = title)
        blast.index_fasta()
        print("successfuly populate")

        '''
        try:
            # remove existing sequences
            blast.sequence_set.all().delete()
            # parse fasta
            #seq_count = 0
            sequence_list = []
            with open(blast.fasta_file.path_full, 'rb') as f:
                offset = 0
                id = ''
                # header = ''
                length = 0
                seq_start_pos = 0
                for line in f:
                    stripped = line.strip()
                    if len(stripped) > 0:
                        if stripped[0] == '>':  # header
                            if length > 0:  # not first sequence, add previous sequence to db
                                sequence_list.append(Sequence(blast_db=blast, id=id, length=length, seq_start_pos=seq_start_pos, seq_end_pos=offset))
                                # seq_count += 1
                            seq_start_pos = offset + line.find('>')  # white chars before '>'
                            # header = stripped[1:] # exclue '>'
                            id = stripped.split(None, 1)[0][1:]
                            length = 0
                        else:  # sequence
                            length += len(stripped)
                    offset += len(line)
                if length > 0:  # add last sequence
                    sequence_list.append(Sequence(blast_db=blast, id=id, length=length, seq_start_pos=seq_start_pos, seq_end_pos=offset))
                    # seq_count += 1
            if len(sequence_list) > 0:
                Sequence.objects.bulk_create(sequence_list)
                return '%d sequences added.' % len(sequence_list)

        except Exception as e:
            return 1, str(e), ''
        '''
