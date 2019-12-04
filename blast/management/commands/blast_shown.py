from blast.models import BlastDb
from django.core.management.base import BaseCommand
import sys

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('BlastDb', nargs='+', type=str, help='enter the blastdb name')
        parser.add_argument('--shown', nargs='*', help= 'make blastdb show or not ex: python manage.py blast_shown [xxx.fa] [xxx.fa] --shown true/false')
    def handle(self,*args,**options):

        n=0;
        title = options['BlastDb']
        for title in title:
            blast2 = BlastDb.objects.filter(title = title)
            print(options)
            n+=1
            if options['shown'][0] == 'true':
                blast2.update(is_shown = True)
            elif options['shown'][0] == 'false':
                blast2.update(is_shown = False)
            else:
                print("please choose  --shown for true or false")
                sys.exit(0)
            print("%d species finished "%n)
        print("all done")
