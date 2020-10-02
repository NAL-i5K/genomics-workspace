from blast.models import BlastQueryRecord
from clustal.models import ClustalQueryRecord
from hmmer.models import HmmerQueryRecord
from datetime import timedelta
from django.utils import timezone

from django.conf import settings
from django.core.management.base import BaseCommand
import django
import os
from shutil import rmtree
from django.core import mail


class Command(BaseCommand):

    def send_email(self, body=["No Message Body"]):
        connection = mail.get_connection()
        try:
            subject = f"Test Results Cleanup Management Command - {timezone.now()}"
            body = "\n".join(body)
            user = os.environ.get('USER')
            domain = os.environ.get('HOSTNAME').split(".",1)[1]
            sender = f'{user}@{domain}'
            email_to = [
                'vernon.chapman@usda.gov',
                #'monica.poelchau@usda.gov',
                #'chris.childers@usda.gov' 
            ]   
            mail.EmailMessage(subject, body, sender, email_to).send()
        except Exception as e:
            print(e)
        finally:
            connection.close()

    def handle(self,*args,**options):

        qr_dirs = 0
        qr_count = 0        
        total_dirs = 0        
        total_records = 0
        time_threshold = timezone.now() - timedelta(days=7)

        body = []
        for QC in [BlastQueryRecord,ClustalQueryRecord, HmmerQueryRecord]:
            class_name = QC.__name__    
            app = QC.__name__.replace("QueryRecord","").lower()        
            try:

                started = timezone.now()
                all_records = QC.objects.all()
                records = all_records.filter(enqueue_date__lte=time_threshold)    
                body.append(f"Started processing {class_name} Objects at {started}")

                processed_records = 0
                processed_dirs = 0
                if all_records.count() <= 0 and records.count() <=  0:
                    body.append(f"No matching {class_name} objects located")
                    body.append(f"Ended processing {class_name} Objects at {timezone.now()}")
                else:
                    body.append(f"Located a total of {all_records.count()} {class_name} Objects")
                    task_path = os.path.join(settings.MEDIA_ROOT,f"{app}/task")
                    for record in records:
                        processed_records += 1
                        task_dir = os.path.join(task_path,record.task_id)

                        if os.path.exists(task_dir) and os.path.isdir(task_dir):
                            rmtree(task_dir, ignore_errors=True)
                            processed_dirs += 1

                        #record.delete()

                    ended = timezone.now()
                    body.append("\n\n")
                    body.append(f"Processed a total of {processed_dirs} {class_name} Directories")
                    body.append(f"Processed a total of {processed_records} {class_name} Records")
                    body.append(f"Ended processing {class_name} Objects at {ended}\n")

                total_dirs += processed_dirs
                total_records += processed_records

            except Exception as e:
                raise e
            finally:
                body.append(f"Total Records:  Located: {total_records}")
                body.append(f"Total Directories: Located: {total_dirs}")
                
        self.send_email(body)
