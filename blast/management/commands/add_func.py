from hmmer.models import HmmerDB
#from django.core.management.base import BaseCommand, CommandError
from app.models import Organism
#import requests
#import os 
import sys

def get_organism(options):

    if len(options['Genus_Species']) == 3:
        organism = options['Genus_Species'][0].lower().capitalize() + ' ' + options['Genus_Species'][1].lower() + ' '+ options['Genus_Species'][2].lower()

    else:
        organism = options['Genus_Species'][0].lower().capitalize() + ' ' + options['Genus_Species'][1].lower()

    organism_database = Organism.objects.get(display_name = organism)
    if organism_database :
        return organism_database
    else:
        print("check your organism name again if it still fails then check your organism database")
        sys.exit(0)
'''
def get_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    path = os.path.join('blast/db',title)
    a=os.path.join(base_dir,'media',path)
    check = os.path.isfile(a)
    if check:
        return path
    else:
         print("No fasta file in media/blast/db")
         sys.exit(0)
'''

