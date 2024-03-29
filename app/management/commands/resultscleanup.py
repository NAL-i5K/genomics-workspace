import os

from datetime import timedelta
from django.core import mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.core.management.base import BaseCommand
from shutil import rmtree

from blast.models import BlastQueryRecord
from clustal.models import ClustalQueryRecord
from hmmer.models import HmmerQueryRecord
import socket
class Command(BaseCommand):

    def send_email(self, body=["No Message Body"]):
        connection = mail.get_connection()
        try:
            subject = f"Results Cleanup Management Command - {timezone.now().strftime('%m/%d/%Y')}"
            body = "\n".join(body)
            user = os.environ.get('USER')
            domain = socket.gethostname().split(".",1)[1]
            sender = f'{user}@{domain}'
            email_to = [
                'vernon.chapman@usda.gov',
                #'monica.poelchau@usda.gov',
                #'chris.childers@usda.gov' 
            ]   
            mail.EmailMessage(subject, body, sender, email_to).send()
        except Exception as e:
            raise e
        finally:
            connection.close()

    def handle(self,*args,**options):
      
        total_dirs = 0        
        total_records = 0
        time_threshold = timezone.now() - timedelta(days=7)

        body = []
        for QC in [BlastQueryRecord,ClustalQueryRecord, HmmerQueryRecord]:
            class_name = QC.__name__    
            app = QC.__name__.replace("QueryRecord","").lower()        
            try:
                # Start Processing
                started = timezone.now()
                body.append(f"Started processing {class_name} Objects at {started.strftime('%H:%M:%S')}")

                # Get all objects and filter
                all_records = QC.objects.all()
                records = all_records.filter(enqueue_date__lte=time_threshold)  

                # Check if any records exist
                if all_records.count() == 0 or records.count() ==  0:
                    body.append(f"No matching {class_name} objects located")
                    ended = timezone.now()
                    elapsed = str(ended - started).split(".")[0]
                    body.append(f"Ended processing {class_name} Objects at {ended.strftime('%H:%M:%S')}\n")
                else:
                    
                    processed_dirs = 0
                    processed_records = 0
                    body.append(f"Located a total of {records.count()} {class_name} Objects")
                    task_path = os.path.join(settings.MEDIA_ROOT,f"{app}/task")

                    # Start Records
                    records_start = timezone.now()
                    for record in records:
                        processed_records += 1
                        task_dir = os.path.join(task_path,record.task_id)
                        if os.path.exists(task_dir) and os.path.isdir(task_dir):
                            rmtree(task_dir, ignore_errors=True)
                            processed_dirs += 1
                    records_end = timezone.now()
                    # End Records

                    elapsed = str(records_end - records_start).split(".")[0]
                    body.append(f"Processed a total of {processed_records} {class_name} Records")
                    if processed_dirs > 0:
                        body.append(f"Processed a total of {processed_dirs} {class_name} Directories")
                    body.append(f"Ended processing {class_name} Objects at {records_end.strftime('%H:%M:%S')}")
                    body.append(f"Processing Time: {elapsed}\n")

                    total_dirs += processed_dirs
                    total_records += processed_records      

                    # Use transaction to delete all matching records at once
                    with transaction.atomic():
                        deleted = records.delete()
                        body.append(f"{deleted}")

            except Exception as e:
                raise e
            finally:
                pass

        body.append(f"Total Records: {total_records}")
        if total_dirs > 0:
            body.append(f"Total Directories: {total_dirs}")

        ended = timezone.now()
        elapsed = str(ended - started).split(".")[0]
        body.append(f"Total Elapsed Time: {elapsed}")
        body.append("\n")
        self.send_email(body)
        
