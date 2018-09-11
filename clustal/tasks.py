from __future__ import absolute_import
from shutil import rmtree
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from subprocess import Popen, PIPE
from datetime import datetime, timedelta
from os import path, chdir, devnull
from pytz import utc
from celery.utils.log import get_task_logger
from celery.signals import task_sent, task_success, task_failure
from django.conf import settings
import json
from clustal.models import ClustalQueryRecord

logger = get_task_logger(__name__)


@shared_task()
def run_clustal_task(task_id, args_list, file_prefix):
    import django
    django.setup()

    logger.info("clustal_task_id: %s" % (task_id,))

    chdir(path.dirname(file_prefix))

    # update dequeue time
    record = ClustalQueryRecord.objects.get(task_id__exact=task_id)
    record.dequeue_date = datetime.utcnow().replace(tzinfo=utc)
    record.save()

    # update status from 'pending' to 'running' for frontend
    with open('status.json', 'r') as f:
        statusdata = json.load(f)
        statusdata['status'] = 'running'

    with open('status.json', 'w') as f:
        json.dump(statusdata, f)

    # run
    FNULL = open(devnull, 'w')
    for args in args_list:
        p = Popen(args, stdout=FNULL, stderr=PIPE)
        p.wait()

    # generate status.json for frontend status checking
    if not path.isfile(file_prefix + '.aln'):
        result_status = "FAILURE"
    else:
        result_status = 'SUCCESS'

    record.result_status = result_status
    record.result_date = datetime.utcnow().replace(tzinfo=utc)
    record.save()

    with open('status.json', 'r') as f:
        statusdata = json.load(f)
        statusdata['status'] = 'done'
    with open('status.json', 'wb') as f:
        json.dump(statusdata, f)

    return task_id  # passed to 'result' argument of task_success_handler


@periodic_task(run_every=(crontab(hour='0', minute='10')))  # Execute daily at midnight
def remove_files():
    logger.info('removing expired files (under test, not working actually)')
    for expired_task in ClustalQueryRecord.objects.filter(result_date__lt=(datetime.utcnow().replace(tzinfo=utc) + timedelta(days=-7))):
        task_path = path.join(settings.MEDIA_ROOT, 'clustal', 'task', expired_task.task_id)
        if path.exists(task_path):
            rmtree(task_path)
            logger.info('removed directory %s' % (task_path))


@task_sent.connect
def task_sent_handler(sender=None, task_id=None, task=None, args=None,
                      kwargs=None, **kwds):
    logger.info('[task_sent] task sent. rabbit task_id: %s' % (task_id))


@task_success.connect
def task_success_handler(sender=None, result=None, **kwds):
    logger.info('[task_success] task done. rabbit task_id: %s.' % (result))


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None,
                         args=None, kwargs=None, traceback=None, einfo=None, **kwds):
    logger.error('[task_failure] task failed. rabbit task_id: %s' % (task_id))
