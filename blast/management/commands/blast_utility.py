from blast.models import BlastDb
from django.core.management.base import BaseCommand
import sys

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('BlastDb', nargs='+', type=str, help='enter the blastdb name')
        parser.add_argument('-m','--makeblastdb', nargs='*', help = 'execute makeblastdb command to specific blastdb')
        parser.add_argument('-p','--populatesequence', nargs='*', help = 'populate specifice blastdb')
        parser.add_argument('--shown', nargs='*', help= 'make blastdb show or not')

    def handle(self,*args,**options):

        n=0;
        title = options['BlastDb']
        print options
        for title in title:
            blast = BlastDb.objects.get(title = title)
            #print blast
            blast2 = BlastDb.objects.filter(title = title)
            #print blast
            n+=1
            if options['makeblastdb'] == []:
                blast.makeblastdb()
            elif options['populatesequence'] == []:
                blast.index_fasta()
            elif options['shown'][0] == 'true':
                blast2.update(is_shown = True)
            elif options['shown'][0] == 'false':
                blast2.update(is_shown = False)
            else:
                print("please choose -m for makeblastd, -p for populate sequence, --shown for True or False")
                sys.exit(0)
            print("%d species finished "%n)
        print("all done")
