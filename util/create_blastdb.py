import sys
from app.models import Organism
from blast.models import BlastDb, SequenceType
from filebrowser.base import FileObject

tax_id = 438503
fasta_file = 'blast/db/forcepstail.consistent.scaffolds.fa'
title = 'test'
description = 'test descrpition'
is_shown = False
dataset_type = 'assembly'
molecule_type = 'nucl'

orgs = Organism.objects.filter(tax_id=tax_id)

if len(orgs) == 0:  # TODO: if no organism exists, create one !
    pass
elif len(orgs) > 1:
    print('Please check the organsms in your database, there are {} organisms with same tax id {}'.format(len(orgs), tax_id))
    sys.exit()
else:  # len(orgs) == 1
    # handle sequence_type
    seq_types = SequenceType.objects.filter(
        molecule_type=molecule_type, dataset_type=dataset_type)

    if len(seq_types) == 0:  # TODO: if no such sequence type exists, create one !
        pass
    elif len(seq_types) > 1:
        print('Please check the organsms in your database, there are {} organisms with same tax id {}'.format(len(orgs), tax_id))
        sys.exit()
    else:  # len(seq_types) == 1
        new_db = BlastDb(fasta_file=FileObject(fasta_file), title=title, description=description, is_shown=is_shown, organism=orgs[0], type=seq_types[0])
        new_db.save()
        returncode, error, output = new_db.makeblastdb()
        returncode, error, output = new_db.index_fasta()
        print(returncode)
        print(error)
