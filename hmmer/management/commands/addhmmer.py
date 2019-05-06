from hmmer.models import HmmerDB
from django.core.management.base import BaseCommand
from app.models import Organism
import os 
import django.db
import sys
path1=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
path=os.path.join(path1,'blast/management/commands')
sys.path.append(path)
from add_func import get_organism

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('Genus_Species',nargs='+',type=str)
        parser.add_argument('-f','--filename',nargs=1,type=str)

    def handle(self,*args,**options):
        '''
        def get_organism():
            
            if len(options['Genus_Species']) == 3:
                organism = options['Genus_Species'][0].lower().capitalize() + ' ' + options['Genus_Species'][1].lower() + ' '+ options['Genus_Species'][2].lower()

            else:
                organism = options['Genus_Species'][0].lower().capitalize() + ' ' + options['Genus_Species'][1].lower()
 
            organism_database = Organism.objects.get(display_name = organism)
            display_name = str(organism_database.display_name)
            #print (type(display_name))
            #print display_name
            if organism == display_name :
                return organism_database
            else:
                print("check your organism name again and if the organism is in the database or not ")
        '''
        def get_path():
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            path = os.path.join('hmmer/db',title)
            a=os.path.join(base_dir,'media',path)
            check = os.path.isfile(a)
            if check:
                return path
            else:
                print("No fasta file in media/hmmer/db")
                sys.exit(0)

        organism = get_organism(options)
        #print options
        if organism:#check whether organism is exist or not

            print organism
            #print(type(organism))
            title = options['filename'][0]
            print title
            fasta_file_path = get_path()
            print fasta_file_path
            #description =
            #try:
            new_db = HmmerDB(organism = organism, fasta_file = fasta_file_path, title = title, description = '', is_shown = True )
            new_db.save()
            print("Success")
            #except django.db.utils.IntegrityError:
                #print("This database already exists")
                #sys.exit(0)
        else :
            pass
            #can use subprocess lib here to add new organism