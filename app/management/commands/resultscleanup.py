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

    def send_email(self, body=[]):
        connection = mail.get_connection()
        try:
            
            
            subject = f"Test Results Cleanup Management Command - {timezone.now()}"
            body = "\n".join(body)
            sender = os.environ.get("HOSTNAME").replace(".","@",1)
            email_to = [
            'vernon.chapman@usda.gov',
            'monica.poelchau@usda.gov',
            'chris.childers@usda.gov' 
            ]   
            mail.EmailMessage(subject, body, sender, email).send()
        except Eception as e:
            pass
        finally:
            connection.close()

    def handle(self,*args,**options):

        time_threshold = timezone.now() - timedelta(days=7)
        qr_count = 0
        qr_dirs = 0
        total_qr_count = 0
        total_qr_dirs = 0
        body = []



        for QC in [BlastQueryRecord,ClustalQueryRecord, HmmerQueryRecord]:
            try:
                records = QC.objects.all().filter(enqueue_date__lte=time_threshold)
                app = QC.__name__.replace("QueryRecord","").lower()
                task_path = os.path.join(settings.MEDIA_ROOT,f"{app}/task")

                if records.count() >= 1:
                    qr_count = records.count()

                    for record in records:
                        task_dir = os.path.join(task_path,record.task_id)
                        if os.path.exists(task_dir) and os.path.isdir(task_dir):
                            rmtree(task_dir, ignore_errors=True)
                            qr_dirs += 1
                    

            except Exceptions as e:
                raise e

            if qr_count > 0:
                total_qr_count += qr_count
                msg = f"Located {qr_count} {QC.__name__} records "
                body.append(msg)
                print(msg)

            if qr_dirs > 0: 
                total_qr_dirs += qr_dirs
                msg = f"Located {qr_dirs} {QC.__name__} task directories "
                body.append(msg)
                print(msg)

        if total_qr_count > 0 or total_qr_dirs > 0) and len(body) > 0:
            body.append("\n\n")
            body.append(f"Total Records:  Located: {total_qr_count} {QC.__name__}")
            body.append(f"Total Directories Located: {total_qr_dirs} {QC.__name__} ")
            self.send_email(body)

