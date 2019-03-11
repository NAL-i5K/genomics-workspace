#from app.models import Organism
#from django.core.management.base import BaseCommand, CommandError
#from django.db import models
import wikipedia
import urllib,json
import requests
#tax_id = 438503
id_baseurl = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&retmode=json&term='
display_name = 'Anoplophora glabripennis'

def short_name():
    short_name = display_name.split(' ')
    short_name1 = short_name[0][0:3]
    short_name2 = short_name[1][0:3]
    short_name = short_name1 + short_name2
    print short_name
    return short_name

'''
#Genetate the organism description
wiki = wikipedia.page(display_name);
description = wiki.summary


'''

def get_taxid ():
    url = id_baseurl+display_name
    #re = urllib.urlopen(url)
    #data = json.loads(re.read())
    re = requests.get(url)
    data = re.json()
    #print data
    tax_id = data['esearchresult']['idlist']
    return tax_id

tax_id = get_taxid()
print tax_id
 # TODO: autogenerate short name / autogenerate tax_id / pull the description from wiki like we did in the GUI
#class Command(BaseCommand):
#    def handle(*args,**options):
#        new_org = Organism(display_name=display_name, short_name=short_name, description=description, tax_id=tax_id)
#        new_org.save
