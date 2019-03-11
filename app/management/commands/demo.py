from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help="adding new organism"

    def handle(self,*args,**options):
        print 'hi sweety'
