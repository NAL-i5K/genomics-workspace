import sys
import requests
from requests.exceptions import HTTPError
from django.db.utils import IntegrityError 
from blast.models import BlastDb, JbrowseSetting
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self,parser):

        parser.add_argument('BlastDB',type=str)
        parser.add_argument('JBrowseURL',type=str)
        parser.add_argument('-c','--check',action="store_true",help='Check the http status')

    def handle(self,*args,**options):

        blast_db_name = options.get("BlastDB")
        jbrowse_url = options.get("JBrowseURL")
        validate = URLValidator()
        try:
            
            blast_db = BlastDb.objects.get(title=blast_db_name)
            validate(jbrowse_url)

            check = options.get("check")
            if check:
                self.stdout.write("Check Status")
                response = requests.head(jbrowse_url)
                if response.status_code != 200:
                    response.raise_for_status()

            new_jbrowse = JbrowseSetting(blast_db=blast_db, url=jbrowse_url )
            new_jbrowse.save()

            self.stdout.write(f"JBrowseSetting Successfully Created.\n")

        except BlastDb.DoesNotExist  as dbe:
            msg = f"[error]: The provided BlastDB '{blast_db_name}' does not exist.\n"
            self.stdout.write(msg)
            sys.exit(1)
        except ValidationError as iurl:
            msg = f"[error]: The provided JBrowseURL '{jbrowse_url}' is invalid.\n"
            self.stdout.write(msg)
            sys.exit(1)
        except HTTPError as err:
            msg = f"[error]: The provided JBrowseURL '{jbrowse_url}' has is unreachable.\n"
            self.stdout.write(msg)
            sys.exit(1)
        except IntegrityError as ie:
            msg = f"[warning]: A JBrowseSetting already exists for {blast_db_name}.\n"
            self.stdout.write(msg)
            sys.exit(1)
