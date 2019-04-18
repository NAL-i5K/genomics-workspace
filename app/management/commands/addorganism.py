from app.models import Organism
from django.core.management.base import BaseCommand
import requests
import django
import os


id_baseurl = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&retmode=json&term='
wiki_url1 = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srprop=snippet&srlimit=1&format=json&srsearch='
wiki_url2 = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=true&titles='

#print tax_id
# TODO: autogenerate short name / autogenerate tax_id / pull the description from wiki like we did in the GUI
class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('Genus_Species',nargs='+',type=str)
        #parser.add_argument('Species',nargs='*',type=str)
        #parser.add_argument('Species2',nargs='?',type=str)
           
    def handle(self,*args,**options):
        
        def display_name():

            if len(options['Genus_Species']) == 2:
                display_name = options['Genus_Species'][0].lower().capitalize() + ' ' + options['Genus_Species'][1].lower()
                return display_name
            else:
                display_name = options['Genus_Species'][0].lower().capitalize()  + ' ' + options['Genus_Species'][1].lower() + ' ' + options['Genus_Species'][2].lower()
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
                    sys.exit(0)
            except requests.exceptions.ConnectionError:
                print("check your internet connection")
                sys.exit(0)

        def get_taxid():
            try:
                url = id_baseurl+display_name
                re = requests.get(url)
                data = re.json()
                tax_id = data['esearchresult']['idlist'][0]
                #print type(tax_id)
                tax_id = int(tax_id)
                #print tax_id
                return tax_id
            except IndexError:
                print("make sure your name is completed and correct")
                sys.exit(0)

        #def main():

        display_name = display_name()
        #print options
        short_name = short_name()
        description = get_description()
        tax_id = get_taxid()
        new_org = Organism(display_name=display_name, short_name=short_name, description=description, tax_id=tax_id)
        file_name = str(display_name)
        os.mknod(file_name)
        #f=open(file_name,'w')
        try:
            new_org.save()
            print("Succeessfully add to database")
        except django.db.utils.IntegrityError:
            print("adding database failed, check if this organism is already in the database and try again")
