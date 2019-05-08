from hmmer.models import HmmerDB
from django.core.management.base import BaseCommand
#from app.models import Organism
import os
#import django.db
import sys
path1=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
path=os.path.join(path1,'blast/management/commands')
sys.path.append(path)
from add_func import get_organism, display_name, get_path

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('Genus_Species',nargs='+',type=str)
        parser.add_argument('-f','--filename',nargs=1,type=str)

    def handle(self,*args,**options):

        name=display_name(options)
        organism = get_organism(name)
        #print options
        if organism:#check whether organism is exist or not

            title = options['filename'][0]
            fasta_file_path = get_path('hmmer',title)
            new_db = HmmerDB(organism = organism, fasta_file = fasta_file_path, title = title, description = '', is_shown = True )
            new_db.save()
            print("Success")
            #except django.db.utils.IntegrityError:
                #print("This database already exists")
                #sys.exit(0)
        else :
            pass
            #can use subprocess lib here to add new organism
