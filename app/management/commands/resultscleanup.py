from blast.models import BlastQueryRecord
from clustal.models import ClustalQueryRecord
from hmmer.models import HmmerQueryRecord
from datetime import timedelta
from django.utils import timezone


from django.core.management.base import BaseCommand
import django

class Command(BaseCommand):

    def handle(self,*args,**options):

        time_threshold = timezone.now() - timedelta(days=7)
        for QC in [BlastQueryRecord,ClustalQueryRecord HmmerQueryRecord]:
            try:
                records = QC.objects.all.filter((entered__gte=time_threshold))
                if records.count() >= 1:
                    print(f"{QC.__class__} => {records.count()}")
                    print(records.first.enqueue_date)
                    

                
            except django.db.utils.IntegrityError:
                print("QueryResults database cleanup failed, check if this organism is already in the database and try again")
