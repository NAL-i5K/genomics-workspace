from blast.models import BlastDb
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('BlastDb', nargs='+', type=str, help='enter the blastdb name')
        parser.add_argument('-m','--makeblastdb', nargs='*', help = 'execute makeblastdb command to specific blastdb')
        parser.add_argument('-p','--populatesequence', nargs='*', help = 'populate specifice blastdb')

    def handle(self,*args,**options):

        n=0;
        title = options['BlastDb']
        for title in title:
            blast = BlastDb.objects.get(title = title)
            n+=1
            if options['makeblastdb'] == []:
                blast.makeblastdb()
            elif options['populatesequence'] == []:
                blast.index_fasta()
            else:
                print("please choose -m for makeblastd and -p for populate sequence")
            print("%d species finished "%n)
        print("all done")
