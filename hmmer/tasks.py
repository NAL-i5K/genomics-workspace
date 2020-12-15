from __future__ import absolute_import
from shutil import rmtree
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from subprocess import Popen, PIPE, call
from datetime import datetime, timedelta
from os import path, chdir
from pytz import utc
from celery.utils.log import get_task_logger
from celery.signals import task_sent, task_success, task_failure
from django.conf import settings
import json
from hmmer.models import HmmerQueryRecord

logger = get_task_logger(__name__)


@shared_task()
def run_hmmer_task(task_id, args_list, file_prefix):
    import django
    django.setup()

    logger.info("hmmer_task_id: %s" % (task_id,))

    chdir(path.dirname(file_prefix))

    # update dequeue time
    record = HmmerQueryRecord.objects.get(task_id__exact=task_id)
    record.dequeue_date = datetime.utcnow().replace(tzinfo=utc)
    record.save()

    # update status from 'pending' to 'running' for frontend
    with open('status.json', 'rt') as f:
        statusdata = json.load(f)
        statusdata['status'] = 'running'
        # db_list = statusdata['db_list']

    with open('status.json', 'wt') as f:
        json.dump(statusdata, f)

    # run
    merge_result_command = 'cat'

    result_status = 'SUCCESS'
    for args in args_list:
        Popen(args, stdin=None, stdout=PIPE).wait()
        if 'hmmbuild' in args[0]:
            if not path.isfile(args[3]):
                result_status = 'FAILURE'
                break
        elif 'hmmsearch' in args[0]:
            merge_result_command = merge_result_command + ' ' + args[2]
            if not path.isfile(args[2]):
                result_status = 'FAILURE'
                break
        elif 'phmmer' in args[0]:
            merge_result_command = merge_result_command + ' ' + args[2]
            if not path.isfile(args[2]):
                result_status = 'FAILURE'
                break

    merge_result_command = merge_result_command + ' > ' + file_prefix + '.merge'

    if(result_status == 'SUCCESS'):
        call(merge_result_command, shell=True)

    record.result_status = result_status
    record.result_date = datetime.utcnow().replace(tzinfo=utc)
    record.save()

    # generate status.json for frontend status checking
    with open('status.json', 'rt') as f:
        statusdata = json.load(f)
        statusdata['status'] = 'done'

    with open('status.json', 'wt') as f:
        json.dump(statusdata, f)

    return task_id  # passed to 'result' argument of task_success_handler


@periodic_task(run_every=(crontab(hour='0', minute='10')))  # Execute daily at midnight
def remove_files():
    logger.info('removing expired files (under test, not working actually)')
    for expired_task in HmmerQueryRecord.objects.filter(result_date__lt=(datetime.utcnow().replace(tzinfo=utc) + timedelta(days=-7))):
        task_path = path.join(settings.MEDIA_ROOT, 'hmmer', 'task', expired_task.task_id)
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
