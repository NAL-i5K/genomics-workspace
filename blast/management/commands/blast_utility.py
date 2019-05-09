from blast.models import BlastDb
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('BlastDb', nargs='+', type=str, help='enter the blastdb name')
        parser.add_argument('-m','--makeblastdb', nargs='*', help = 'execute makeblastdb command to specific blastdb')
        parser.add_argument('-p','--populatesequence', nargs='*', help = 'populate specifice blastdb')

    def handle(self,*args,**options):

        title = options['BlastDb'][0]
        blast = BlastDb.objects.get(title = title)
        if options['makeblastdb'] == []:
            blast.makeblastdb()
            print("done")
        elif options['populatesequence'] == []:
            blast.index_fasta()
            print("done")
        else:
            print("please choose -m for makeblastd and -p for populate sequence")
