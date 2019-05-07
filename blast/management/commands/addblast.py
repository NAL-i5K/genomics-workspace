from blast.models import BlastDb,SequenceType
from django.core.management.base import BaseCommand
#from app.models import Organism
import sys
import os
#sys.path.append('genomics-workspace/app/management/commands/add_func.py')
from add_func import get_organism, display_name, get_path

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('Genus_Species',nargs='+',type=str)
        parser.add_argument('-t','--type',nargs='+',type=str,help='please enter nucleotide or peptide and enter Genome Assembly or Protein or Transcript')
        parser.add_argument('-f','--filename',nargs=1,type=str)

    def handle(self,*args,**options):

        '''
        def get_organism():

            if len(options['Genus_Species']) == 3:
                organism = options['Genus_Species'][0].lower().capitalize() + ' ' + options['Genus_Species'][1].lower() + ' '+ options['Genus_Species'][2].lower()

            else:
                organism = options['Genus_Species'][0].lower().capitalize() + ' ' + options['Genus_Species'][1].lower()

            organism_database = Organism.objects.get(display_name = organism)
            #print (type(display_name))
            #print display_name
            if organism_database :
                return organism_database
            else:
                print("check your organism name again if it still fails then check your organism database")
                sys.exit(0)
        '''
        def get_type(): #get the sequence type from SequencType Table
            try:
                molecule = options['type'][0].lower() #get molecule_type from command line
                if molecule == 'peptide':    #change the name tp prot or nucl
                    molecule2 = 'prot'
                elif molecule == 'nucleotide':
                    molecule2 = 'nucl'
                else:
                    print("please enter the correct molecule_type, must be nucleotide or peptide")
                    sys.exit(0)
            except Exception :
                print("enter the argument complete '-t' '-f' ")
                sys.exit(0)
            molecule_type = SequenceType.objects.filter(molecule_type = molecule2) #get the data from molecule_type field
            a = molecule_type[0]
            molecule_str = a.molecule_type
            print(molecule_str) #print the name of molecule_type after translating

            if len(options['type']) == 2:
                dataset = options['type'][1].lower().capitalize()
                if dataset == 'Transcript' or dataset == 'Protein':
                    print(dataset)
                else :
                    print("check your dataset_type, must be Protein or Transcript or Genome Assembly")
                    sys.exit(0)
            elif len(options['type']) == 3:
                dataset = options['type'][1].lower().capitalize() +' '+options['type'][2].lower().capitalize()
                if dataset == 'Genome Assembly':
                    pass
                    #print(dataset)
                else:
                    print("check your dataset_type, must be Protein or Transcript or Genome Assembly")
                    sys.exit(0)

            dataset_type = SequenceType.objects.filter(dataset_type = dataset)
            #print dataset_type
            b = dataset_type[0]
            dataset_str = str(b.dataset_type)

            if molecule2 == molecule_str and dataset == dataset_str :
                dataset_type = SequenceType.objects.filter(molecule_type = molecule2, dataset_type = dataset)
                if len(dataset_type)== 0:
                    print("there are no {molecule} - {dataset} combination in the database".format(molecule=molecule.capitalize(),dataset=dataset_str))
                    sys.exit(0)
                else:
                    return dataset_type[0]

            else:
                print("something wrong in get_type")
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
        print(options)
        name=display_name(options)
        organism = get_organism(name)
        if organism:#check whether organism is exist or not

            blast_type = get_type()
            #print blast_type
            title = options['filename'][0]
            fasta_file_path = get_path('blast',title)
            print fasta_file_path
            #try:
            #os.mknod(title)
            new_db = BlastDb(organism = organism, type = blast_type, fasta_file = fasta_file_path, title = title, description = '', is_shown = True )
            new_db.save()
            print("you can move to makeblastdb and populate sequence step")
            #except django.db.utils.IntegrityError:
                #print("This database already exists")
                #sys.exit(0)
        else :
            pass
            #TODO can use subprocess lib here to add new organism
