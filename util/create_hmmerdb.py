import sys
from app.models import Organism
from hmmer.models import HmmerDB


tax_id = 438503
fasta_file = 'blast/db/forcepstail.consistent.scaffolds.fa'  # path after media/ folder
title = 'test'
description = 'test descro[topn'
is_shown = False

orgs = Organism.objects.filter(tax_id=tax_id)

if len(orgs) == 0:  # TODO: if no organism exists, create one !
    pass
elif len(orgs) > 1:
    print('Please check the organsms in your database, there are {} organisms with same tax id {}'.format(len(orgs), tax_id))
    sys.exit()
else:  # len(orgs) == 1
    new_db = HmmerDB(tax_id=tax_id, fasta_file=fasta_file, title=title, description=description, is_shown=is_shown, organism=orgs[0])
    new_db.save()
