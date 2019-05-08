from blast.models import BlastDb
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('BlastDb', nargs='+', type=str, help='enter the blastdb name')

    def handle(self,*args,**options):
        title = options['BlastDb'][0]
        blast = BlastDb.objects.get(title = title)
        blast.makeblastdb()
        print("done")
