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
class Command(BaseCommand):

    def handle(self,*args,**options):

        time_threshold = timezone.now() - timedelta(days=7)
        qr_count = 0
        qr_dirs = 0
        totoal_qr_count = 0
        totoal_qr_dirs = 0

        for QC in [BlastQueryRecord,ClustalQueryRecord, HmmerQueryRecord]:
            try:
                records = QC.objects.all().filter(enqueue_date__gte=time_threshold)
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
                totoal_qr_count += qr_count
                print(f"Located {qr_count} {QC.__name__} records ")

            if qr_dirs > 0: 
                totoal_qrqr_dirs += qrqr_dirs
                print(f"Located {qr_dirs} {QC.__name__} task directories ")

        print(f"Total Records:  Located: {totoal_qr_count} {QC.__name__}")
        print(f"Total Directories Located: {totoal_qr_dirs} {QC.__name__} ")


            
