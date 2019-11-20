from blast.models import BlastDb
from django.core.management.base import BaseCommand
import sys

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('BlastDb', nargs='+', type=str, help='enter the blastdb name')
        parser.add_argument('-m','--makeblastdb', nargs='*', help = 'execute makeblastdb command to specific blastdb, ex: python manage.py blast_utility [xxx.fa] [xxx.fa] -m')
        parser.add_argument('-p','--populatesequence', nargs='*', help = 'populate specifice blastdb, ex: python manage.py blast_utility [xxx.fa] [xxx.fa] -p')
        #parser.add_argument('--shown', nargs='*', help= 'make blastdb show or not ex: python manage.py blast_utility [xxx.fa] [xxx.fa] --shown true/false')

    def handle(self,*args,**options):

        n=0;
        title = options['BlastDb']
        for title in title:
            blast = BlastDb.objects.get(title = title)
            #print blast
            n+=1
            if options['makeblastdb'] == []:
                blast.makeblastdb()
            elif options['populatesequence'] == []:
                blast.index_fasta()
            else:
                print("please choose -m for makeblastd, -p for populate sequence, --shown for true or false")
                sys.exit(0)
            print("%d species finished "%n)
        print("all done")
