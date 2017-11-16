from __future__ import absolute_import
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.conf import settings
from django.core.cache import cache
from uuid import uuid4
from os import path, makedirs, chmod, remove, symlink
from sys import platform
from .tasks import run_hmmer_task
from .models import HmmerQueryRecord, HmmerDB
from datetime import datetime, timedelta
from pytz import timezone
from django.utils.timezone import localtime, now
import json
import traceback
import stat as Perm
from itertools import groupby
from subprocess import Popen, PIPE
from i5k.settings import HMMER_QUERY_MAX


def manual(request):
    '''
    Manual page of Hmmer
    '''
    return render(request, 'hmmer/manual.html',{'title':'HMMER Manual'})

def create(request):
    '''
    Main page of Hmmer
    Use hmmsearch fast mode for format validation

    Input limitation:
    (1). Phmmer, Max number of query sequences: 10 sequences
    '''
    if request.method == 'GET':
        hmmerdb_list = sorted([['Protein', "Protein", db.title, db.organism.display_name, db.description] for db in
                               HmmerDB.objects.select_related('organism').filter(is_shown=True)],
                              key=lambda x: (x[3], x[1], x[0], x[2]))
        hmmerdb_type_counts = dict([(k.lower().replace(' ', '_'), len(list(g))) for k, g in
                                    groupby(sorted(hmmerdb_list, key=lambda x: x[0]), key=lambda x: x[0])])


        '''
        Redirect from clustal result
        '''
        clustal_content = []
        if ("clustal_task_id" in request.GET):
            clustal_aln = path.join(settings.MEDIA_ROOT, 'clustal',
                                    'task', request.GET['clustal_task_id'],
                                    request.GET['clustal_task_id'] + ".aln")

            with open(clustal_aln, 'r') as content_file:
                for line in content_file:
                    clustal_content.append(line)

        return render(request, 'hmmer/main.html', {
            'title': 'HMMER Query',
            'hmmerdb_list': json.dumps(hmmerdb_list),
            'hmmerdb_type_counts': hmmerdb_type_counts,
            'clustal_content': "".join(clustal_content),
        })

    elif request.method == 'POST':
        # setup file paths

        task_id = uuid4().hex
        task_dir = path.join(settings.MEDIA_ROOT, 'hmmer', 'task', task_id)
        # file_prefix only for task...
        file_prefix = path.join(settings.MEDIA_ROOT, 'hmmer', 'task', task_id, task_id)
        if not path.exists(task_dir):
            makedirs(task_dir)

        chmod(task_dir,
              Perm.S_IRWXU | Perm.S_IRWXG | Perm.S_IRWXO)
        # ensure the standalone dequeuing process can open files in the directory
        # change directory to task directory

        if 'query-file' in request.FILES:
            query_filename = path.join(settings.MEDIA_ROOT, 'hmmer', 'task', task_id, request.FILES['query-file'].name)
            with open(query_filename, 'wb') as query_f:
                for chunk in request.FILES['query-file'].chunks():
                    query_f.write(chunk)
        elif 'query-sequence' in request.POST and request.POST['query-sequence']:
            query_filename = path.join(settings.MEDIA_ROOT, 'hmmer', 'task', task_id, task_id + '.in')
            with open(query_filename, 'wb') as query_f:
                query_text = [x.encode('ascii','ignore').strip() for x in request.POST['query-sequence'].split('\n')]
                query_f.write('\n'.join(query_text))
        else:
            return render(request, 'hmmer/invalid_query.html', {'title': '', })

        chmod(query_filename,
              Perm.S_IRWXU | Perm.S_IRWXG | Perm.S_IRWXO)
        # ensure the standalone dequeuing process can access the file

        bin_name = 'bin_linux'
        if platform == 'darwin':
            bin_name = 'bin_mac'
        program_path = path.join(settings.PROJECT_ROOT, 'hmmer', bin_name)

        if request.POST['program'] == 'phmmer':
            with open(query_filename, 'r') as f:
                qstr = f.read()
                if qstr.count('>') > int(HMMER_QUERY_MAX):
                    query_cnt = str(qstr.count('>'))
                    remove(query_filename)
                    return render(request, 'hmmer/invalid_query.html',
                            {'title': 'Your search includes ' + query_cnt + ' sequences, but HMMER allows a maximum of ' + str(HMMER_QUERY_MAX) + ' sequences per submission.', })
        elif request.POST['program'] == 'hmmsearch':
            '''
            Format validation by hmmsearch fast mode
            If the machine can't perform it in short time, it could be marked.
            But you need find a good to check format in front-end
            '''
            p = Popen([path.join(program_path, "hmmbuild"), "--fast", '--amino',
                      path.join(settings.MEDIA_ROOT, 'hmmer', 'task', 'hmmbuild.test'), query_filename],
                      stdout=PIPE, stderr=PIPE)
            p.wait()
            result = p.communicate()[1]
            if(result != ''):
                return render(request, 'hmmer/invalid_query.html',
                             {'title': 'Invalid MSA format',
                              'info' :'<a href="http://toolkit.tuebingen.mpg.de/reformat/help_params#format" target="_blank"> \
                                      Valid MSA format descriptions </a>' })
        else:  # check if program is in list for security
            raise Http404

        # build hmmer command
        db_list = ' '.join(
            [db.fasta_file.path_full for db in HmmerDB.objects.filter(title__in=set(request.POST.getlist('db-name')))])
        for db in db_list.split(' '):
            symlink(db, path.join(settings.MEDIA_ROOT, 'hmmer', 'task', task_id, db[db.rindex('/') + 1:]))

        if not db_list:
            return render(request, 'hmmer/invalid_query.html', {'title': '', })

        if request.POST['cutoff'] == 'evalue':
            option_params = ['--incE', request.POST['s_sequence'], '--incdomE', request.POST['s_hit'],
                             '-E', request.POST['r_sequence'], '--domE', request.POST['r_hit']]
        elif request.POST['cutoff'] == 'bitscore':
            option_params = ['--incT', request.POST['s_sequence'], '--incdomT', request.POST['s_hit'],
                             '-T', request.POST['r_sequence'], '--domT', request.POST['r_hit']]
        else:
            raise Http404

        record = HmmerQueryRecord()
        record.task_id = task_id
        if request.user.is_authenticated():
            record.user = request.user
        record.save()
        # generate status.json for frontend statu checking
        with open(query_filename, 'r') as f:
            qstr = f.read()
            seq_count = qstr.count('>')
            if (seq_count == 0):
                seq_count = 1
            with open(path.join(settings.MEDIA_ROOT, 'hmmer', 'task', task_id, 'status.json'), 'wb') as f:
                json.dump({'status': 'pending', 'seq_count': seq_count,
                           'db_list': [db[db.rindex('/') + 1:] for db in db_list.split(' ')],
                           'program': request.POST['program'],
                           'params': option_params,
                           'input': path.basename(query_filename)}, f)
        args_list = generate_hmmer_args_list(request.POST['program'], program_path, query_filename, option_params, db_list)
        run_hmmer_task.delay(task_id, args_list, file_prefix)
        return redirect('hmmer:retrieve', task_id)


def retrieve(request, task_id='1'):
    '''
    Retrieve output fo Hmmer tasks
    '''
    try:
        r = HmmerQueryRecord.objects.get(task_id=task_id)
        # if result is generated and not expired
        if r.result_date and (r.result_date.replace(tzinfo=None) >= (datetime.utcnow() + timedelta(days=-7))):
            url_base_prefix = path.join(settings.MEDIA_URL, 'hmmer', 'task', task_id)
            dir_base_prefix = path.join(settings.MEDIA_ROOT, 'hmmer', 'task', task_id)
            url_prefix = path.join(url_base_prefix, task_id)
            dir_prefix = path.join(dir_base_prefix, task_id)

            with open(path.join(dir_base_prefix, 'status.json'), 'r') as f:
                statusdata = json.load(f)
                db_list = statusdata['db_list']
                file_in = path.join(url_base_prefix, statusdata['input'])

            out_txt = []
            report = ["<br>"]

            # 1mb limitation
            if path.isfile(dir_prefix + '.merge') and path.getsize(dir_prefix + '.merge') > 1024000:
                out_txt = 'The Hmmer reports exceed 1 Megabyte, please download it.'
                isExceed = True
            else:
                isExceed = False
                # '[ok]' is the end line of each hmmer output (delimiter for different dbs)
                with open(dir_prefix + ".merge", 'r') as content_file:
                    for line in content_file:
                        line = line.rstrip('\n')
                        if line == '[ok]':
                            out_txt.append(''.join(report).replace(' ', '&nbsp;'))
                            report = ["<br>"]
                        else:
                            report.append(line + "<br>")

            if r.result_status == 'SUCCESS':
                return render(
                    request,
                    'hmmer/result.html', {
                        'title': 'HMMER Result',
                        'output': url_prefix + '.merge',
                        'status': path.join(url_base_prefix, 'status.json'),
                        'input': file_in,
                        'options': db_list,  # for interation in result page
                        'report': out_txt,
                        'task_id': task_id,
                        'isExceed': isExceed
                    })
            else:
                return render(request, 'hmmer/results_not_existed.html',
                              {
                                  'title': 'No Hits Found',
                                  'isNoHits': True,
                                  'isExpired': False,
                              })
        else:
            enqueue_date = r.enqueue_date.astimezone(timezone('US/Eastern')).strftime('%d %b %Y %X %Z')
            if r.dequeue_date:
                dequeue_date = r.dequeue_date.astimezone(timezone('US/Eastern')).strftime('%d %b %Y %X %Z')
            else:
                dequeue_date = None
            # result is exipired
            isExpired = False
            if r.result_date and (r.result_date.replace(tzinfo=None) < (datetime.utcnow() + timedelta(days=-7))):
                isExpired = True
            return render(request, 'hmmer/results_not_existed.html', {
                'title': 'Query Submitted',
                'task_id': task_id,
                'isExpired': isExpired,
                'enqueue_date': enqueue_date,
                'dequeue_date': dequeue_date,
                'isNoHits': False,
            })
    except:
        if settings.USE_PROD_SETTINGS:
            raise Http404
        else:
            return HttpResponse(traceback.format_exc())


def status(request, task_id):
    if request.method == 'GET':
        status_file_path = path.join(settings.MEDIA_ROOT, 'hmmer', 'task', task_id, 'status.json')
        status = {'status': 'unknown'}
        if path.isfile(status_file_path):
            with open(status_file_path, 'rb') as f:
                statusdata = json.load(f)
                if statusdata['status'] == 'pending' and settings.USE_CACHE:
                    tlist = cache.get('task_list_cache', [])
                    num_preceding = -1
                    if tlist:
                        for index, tuple in enumerate(tlist):
                            if task_id in tuple:
                                num_preceding = index
                                break
                    statusdata['num_preceding'] = num_preceding
                elif statusdata['status'] == 'running':
                    statusdata['processed'] = 0
                return HttpResponse(json.dumps(statusdata))
        return HttpResponse(json.dumps(status))
    else:
        return HttpResponse('Invalid Post')

# to-do: integrate with existing router of restframework
from rest_framework.renderers import JSONRenderer
from .serializers import UserHmmerQueryRecordSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def user_tasks(request, user_id):
    """
    Return tasks performed by the user.
    """
    if request.method == 'GET':
        records = HmmerQueryRecord.objects.filter(user__id=user_id, result_date__gt=(localtime(now())+ timedelta(days=-7)))
        serializer = UserHmmerQueryRecordSerializer(records, many=True)
        return JSONResponse(serializer.data)


def generate_hmmer_args_list(program, program_path, query_filename, option_params, db_list):
    args_list = []
    if program == 'hmmsearch':
        args_list.append([path.join(program_path, 'hmmbuild'), '--amino', '-o', 'hmm.sumary',
            path.basename(query_filename) + '.hmm', path.basename(query_filename)])
        for idx, db in enumerate(db_list.split()):
            args_list.append([path.join(program_path, 'hmmsearch'), '-o', str(idx) + '.out']
                    + option_params + [path.basename(query_filename) + '.hmm', path.basename(db)])
    else:  # phmmer
        for idx, db in enumerate(db_list.split()):
            args_list.append([path.join(program_path, 'phmmer'), '-o', str(idx) + '.out']
                    + option_params + [path.basename(query_filename), path.basename(db)])
    return args_list
