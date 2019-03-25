from app.models import Organism
from django.core.management.base import BaseCommand, CommandError
from django.db import models
import urllib,json
import requests
import argparse
import django

#parser = argparse.ArgumentParser()
#parser.add_argument("Genus",help='type the display_name for your organism')
#parser.add_argument("Species")
#parser.add_argument("-o","--optional-arg",help="optional argument",dest="opc")
#args = parser.parse_args()
#print args.opc
id_baseurl = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&retmode=json&term='
#display_name = args.Genus + ' ' + args.Species#'Anoplophora_glabripennis'
#print display_name
#Genetate the organism description
wiki_url1 = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srprop=snippet&srlimit=1&format=json&srsearch='
wiki_url2 = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=true&titles='


#print tax_id
# TODO: autogenerate short name / autogenerate tax_id / pull the description from wiki like we did in the GUI
class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('Genus',nargs=1,type=str)
        parser.add_argument('Species',nargs=1,type=str)
        parser.add_argument('Species2',nargs='?',type=str)
           
    def handle(*args,**options):

        def display_name():
            if options['Species2'] is None	:
                display_name=options['Genus'][0]+' '+options['Species'][0]
                return display_name
            else:
                display_name=options['Genus'][0]+' '+options['Species'][0]+' '+options['Species2']
                return display_name

        def short_name():
            short_name = display_name.split(' ')
            short_name1 = short_name[0][0:3]
            short_name2 = short_name[1][0:3]
            short_name = short_name1 + short_name2
            #print short_name
            return short_name


        def get_description():
            url1 = wiki_url1 + display_name
            #re1 = urllib.urlopen(url1)
            #data1 = json.loads(re1.read())  
            try: 
            
                re1 = requests.get(url1)
                data1 = re1.json()
                #print type(data1)
                try:
                    title = data1['query']['search'][0]['title']
                #re1.encoding = 'utf8'
    
                    url2 = wiki_url2 + title
                    re2 = requests.get(url2)
                    #print re2.text
                    data2 = re2.json()
                    key = data1['query']['search'][0]['pageid']    
                    #print type(key)
                    key = str(key)
                    #print type(key)
                    description = data2['query']['pages'][key]['extract']    
                    #print description
                    return description
                except 	IndexError:
                    print("check your organism name again")
            except requests.exceptions.ConnectionError:
                #print("check your internet connection")

        def get_taxid():
            try:
                url = id_baseurl+display_name
                #re = urllib.urlopen(url)
                #data = json.loads(re.read())
                re = requests.get(url)
                data = re.json()
                tax_id = data['esearchresult']['idlist'][0]
                #print type(tax_id)
                tax_id = int(tax_id)
                #print tax_id
                return tax_id
            except IndexError:
                print("make sure your name is completed and correct")      
        #print options
        #print type(options['Genus'])
        #print type(options['Species'])
        #print type(options['Species2'])
        ##print options['Species2']
        display_name = display_name()
        #print display_name
        short_name = short_name()
        description = get_description()
        tax_id = get_taxid()
        
        new_org = Organism(display_name=display_name, short_name=short_name, description=description, tax_id=tax_id)
        try:
            new_org.save()
            print("Succeessfully added species")
        except django.db.utils.IntegrityError:
            print("adding database failed, please try again")
