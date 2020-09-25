from blast.models import BlastQueryRecord
from clustal.models import ClustalQueryRecord
from hmmer.models import HmmerQueryRecord
from datetime import timedelta
from django.utils import timezone

from django.conf import settings
from django.core.management.base import BaseCommand
import django
import os
class Command(BaseCommand):

    def handle(self,*args,**options):

        time_threshold = timezone.now() - timedelta(days=7)
        for QC in [BlastQueryRecord,ClustalQueryRecord, HmmerQueryRecord]:
            try:
                records = QC.objects.all().filter(enqueue_date__gte=time_threshold)
                app = QC.__name__.replace("QueryRecord","").lower()
                task_path = os.path.join(settings.MEDIA_ROOT,f"{app}/task")

                if records.count() >= 1:
                    for record in records:
                        task_dir = os.path.join(task_path,record.task_id)
                        if os.path.exists(task_dir):
                            print(task_dir)
            except Exceptions as e:
                raise e
