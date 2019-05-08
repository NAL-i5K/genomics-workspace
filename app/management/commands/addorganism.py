from app.models import Organism
from django.core.management.base import BaseCommand
import requests
import django
import os
import sys
from add_func import display_name, short_name, get_description, get_taxid

id_baseurl = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&retmode=json&term='
wiki_url1 = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srprop=snippet&srlimit=1&format=json&srsearch='
wiki_url2 = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=true&titles='

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('Genus_Species',nargs='+',type=str)
        #parser.add_argument('Species',nargs='*',type=str)
        #parser.add_argument('Species2',nargs='?',type=str)
           
    def handle(self,*args,**options):

        name = display_name(options)
        shortname = short_name(name)
        url1 = wiki_url1 + name
        description = get_description(url1,wiki_url2)
        tax_id = get_taxid(id_baseurl,name)
        new_org = Organism(display_name=name, short_name=shortname, description=description, tax_id=tax_id)

        try:
            new_org.save()
            print("Succeessfully add to database")
        except django.db.utils.IntegrityError:
            print("adding database failed, check if this organism is already in the database and try again")
