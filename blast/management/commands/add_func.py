#from hmmer.models import HmmerDB
#from django.core.management.base import BaseCommand, CommandError
from app.models import Organism
#import requests
import os
import sys

def display_name(options):

    if len(options['Genus_Species']) == 3:
        display_name = options['Genus_Species'][0].lower().capitalize() + ' ' + options['Genus_Species'][1].lower() + ' '+ options['Genus_Species'][2].lower()
        return display_name

    else:
        display_name = options['Genus_Species'][0].lower().capitalize() + ' ' + options['Genus_Species'][1].lower()
        return display_name

def get_organism(display_name):

    organism_database = Organism.objects.get(display_name = display_name)
    if organism_database :
        return organism_database
    else:
        print("check your organism name again if it still fails then check your organism database")
        sys.exit(0)

def get_path(app_name,title):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    if app_name == 'blast':
        path = os.path.join('blast/db',title)
    else:
        path = os.path.join('hmmer/db',title)
    
    a=os.path.join(base_dir,'media',path)
    check = os.path.isfile(a)
    if check:
        return path
    else:
        print("No fasta file in media/blast/db or media/hmmer/db")
        sys.exit(0)	
