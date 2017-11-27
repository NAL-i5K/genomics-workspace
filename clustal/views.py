from __future__ import absolute_import
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponse
from django.conf import settings
from django.core.cache import cache
from uuid import uuid4
from os import path, makedirs, chmod
from .tasks import run_clustal_task
from .models import ClustalQueryRecord, ClustalSearch
from datetime import datetime, timedelta
from pytz import timezone
from django.utils.timezone import localtime, now
from misc.logger import i5kLogger
from misc.get_tag import get_tag
import json
import traceback
import stat as Perm

log = i5kLogger()

def manual(request):
    '''
    Manual page of Clustal
    '''
    return render(request, 'clustal/manual.html', {'title':'Clustal Manual'})

def create(request):
    '''
    Main page of Clustal
    * Max number of query sequences: 600 sequences
    '''
    if request.method == 'GET':

        if 'search_id' in request.GET and request.GET['search_id']:
            tag = request.GET['search_id']
            saved_search = ClustalSearch.objects.filter(search_tag=tag)
            if saved_search:
                saved_search = saved_search[0]
                #sequence_list = saved_search.sequence.split('\n')
                return render(request, 'clustal/main.html', {
                    'tag':               saved_search.search_tag,
                    'sequence':          saved_search.sequence,
                    'program':           saved_search.program,
                    'pairwise':          saved_search.pairwise,
                    'sequence_type':     saved_search.sequence_type,
                    'pwdnamatrix':       saved_search.pwdnamatrix,
                    'dna_pwgapopen':     saved_search.dna_pwgapopen,
                    'dna_pwgapext':      saved_search.dna_pwgapext,
                    'pwmatrix':          saved_search.pwmatrix,
                    'protein_pwgapopen': saved_search.protein_pwgapopen,
                    'protein_pwgapext':  saved_search.protein_pwgapext,
                    'ktuple':            saved_search.ktuple,
                    'window':            saved_search.window,
                    'pairgap':           saved_search.pairgap,
                    'topdiags':          saved_search.topdiags,
                    'score':             saved_search.score,
                    'dnamatrix':         saved_search.dnamatrix,
                    'dna_gapopen':       saved_search.dna_gapopen,
                    'dna_gapext':        saved_search.dna_gapext,
                    'dna_gapdist':       saved_search.dna_gapdist,
                    'dna_iteration':     saved_search.dna_iteration,
                    'dna_numiter':       saved_search.dna_numiter,
                    'dna_clustering':    saved_search.dna_clustering,
                    'matrix':            saved_search.matrix,
                    'protein_gapopen':   saved_search.protein_gapopen,
                    'protein_gapext':    saved_search.protein_gapext,
                    'protein_gapdist':   saved_search.protein_gapdist,
                    'protein_iteration': saved_search.protein_iteration,
                    'protein_numiter':   saved_search.protein_numiter,
                    'protein_clustering': saved_search.protein_clustering,
                    'output':            saved_search.output,
                    'outorder':          saved_search.outorder,
                    'dealing_input':     saved_search.dealing_input,
                    'clustering_guide_tree':  saved_search.clustering_guide_tree,
                    'clustering_guide_iter':  saved_search.clustering_guide_iter,
                    'combined_iter':     saved_search.combined_iter,
                    'max_gt_iter':       saved_search.max_gt_iter,
                    'max_hmm_iter':      saved_search.max_hmm_iter,
                    'omega_output':      saved_search.omega_output,
                    'omega_order':       saved_search.omega_order,
                    'title':           'Clustal Query',
                })

        tag = get_tag('vagrant', ClustalSearch)
        return render(request, 'clustal/main.html', {
            'tag': tag,
            'title': 'Clustal Query',
        })
    elif request.method == 'POST':
        # setup file paths
        task_id = uuid4().hex
        task_dir = path.join(settings.MEDIA_ROOT, 'clustal', 'task', task_id)
        # file_prefix only for task...
        file_prefix = path.join(settings.MEDIA_ROOT, 'clustal', 'task', task_id, task_id)
        if not path.exists(task_dir):
            makedirs(task_dir)
        chmod(task_dir, Perm.S_IRWXU | Perm.S_IRWXG | Perm.S_IRWXO) 
        # ensure the standalone dequeuing process can open files in the directory
        # change directory to task directory

        query_filename = ''
        if 'query-file' in request.FILES:
            query_filename = path.join(settings.MEDIA_ROOT, 'clustal', 'task', task_id, request.FILES['query-file'].name)
            with open(query_filename, 'wb') as query_f:
                for chunk in request.FILES['query-file'].chunks():
                    query_f.write(chunk)
        elif 'query-sequence' in request.POST and request.POST['query-sequence']:
            query_filename = path.join(settings.MEDIA_ROOT, 'clustal', 'task', task_id, task_id + '.in')
            with open(query_filename, 'wb') as query_f:
                query_text = [x.encode('ascii','ignore').strip() for x in request.POST['query-sequence'].split('\n')]
                query_f.write('\n'.join(query_text))
        else:
            return render(request, 'clustal/invalid_query.html', {'title': '',})

        chmod(query_filename, Perm.S_IRWXU | Perm.S_IRWXG | Perm.S_IRWXO) 
        # ensure the standalone dequeuing process can access the file

        bin_name = 'bin_linux'
        program_path = path.join(settings.PROJECT_ROOT, 'clustal', bin_name)

        # count number of query sequence by counting '>'
        with open(query_filename, 'r') as f:
            qstr = f.read()
            seq_count = qstr.count('>')
            if(seq_count > 600):
                return render(request, 'clustal/invalid_query.html', 
                        {'title': 'Clustal: Max number of query sequences: 600 sequences.',})

        is_color = False
        # check if program is in list for security
        if request.POST['program'] in ['clustalw','clustalo']:

            option_params = []
            args_list = []

            if request.POST['program'] == 'clustalw':
                #clustalw
                option_params.append("-type="+request.POST['sequenceType'])

                #parameters setting for full option or fast option
                if request.POST['pairwise'] == "full":
                    if request.POST['sequenceType'] == "dna":
                        if request.POST['pwdnamatrix'] != "":
                            option_params.append('-PWDNAMATRIX='+request.POST['pwdnamatrix'])
                        if request.POST['dna_pwgapopen'] != "":
                            option_params.append('-PWGAPOPEN='+request.POST['dna_pwgapopen'])
                        if request.POST['dna_pwgapext'] != "":
                            option_params.append('-PWGAPEXT='+request.POST['dna_pwgapext'])
                    elif request.POST['sequenceType'] == "protein":
                        if request.POST['pwmatrix'] != "":
                            option_params.append('-PWMATRIX='+request.POST['pwmatrix'])
                        if request.POST['protein_pwgapopen'] != "":
                            option_params.append('-PWGAPOPEN='+request.POST['protein_pwgapopen'])
                        if request.POST['protein_pwgapopen'] != "":
                            option_params.append('-PWGAPEXT='+request.POST['protein_pwgapext'])
                elif request.POST['pairwise'] == "fast":
                    option_params.append('-QUICKTREE')
                    if request.POST['ktuple'] != "":
                        option_params.append('-KTUPLE='+request.POST['ktuple'])
                    if request.POST['window'] != "":
                        option_params.append('-WINDOW='+request.POST['window'])
                    if request.POST['pairgap'] != "":
                        option_params.append('-PAIRGAP='+request.POST['pairgap'])
                    if request.POST['topdiags'] != "":
                        option_params.append('-TOPDIAGS='+request.POST['topdiags'])
                    if request.POST['score'] != "":
                        option_params.append('-SCORE='+request.POST['score'])

                #prarmeters setting for mutliple alignment
                if request.POST['sequenceType'] == "dna":
                    if request.POST['dnamatrix'] != "":
                        option_params.append('-DNAMATRIX='+request.POST['dnamatrix'])
                    if request.POST['dna_gapopen'] != "":
                        option_params.append('-GAPOPEN='+request.POST['dna_gapopen'])
                    if request.POST['dna_gapext'] != "":
                        option_params.append('-GAPEXT='+request.POST['dna_gapext'])
                    if request.POST['dna_gapdist'] != "":
                        option_params.append('-GAPDIST='+request.POST['dna_gapdist'])
                    if request.POST['dna_iteration'] != "":
                        option_params.append('-ITERATION='+request.POST['dna_iteration'])
                    if request.POST['dna_numiter'] != "":
                        option_params.append('-NUMITER='+request.POST['dna_numiter'])
                    if request.POST['dna_clustering'] != "":
                        option_params.append('-CLUSTERING='+request.POST['dna_clustering'])
                elif request.POST['sequenceType'] == "protein":
                    if request.POST['matrix'] != "":
                        option_params.append('-MATRIX='+request.POST['matrix'])
                    if request.POST['protein_gapopen'] != "":
                        option_params.append('-GAPOPEN='+request.POST['protein_gapopen'])
                    if request.POST['protein_gapext'] != "":
                        option_params.append('-GAPEXT='+request.POST['protein_gapext'])
                    if request.POST['protein_gapdist'] != "":
                        option_params.append('-GAPDIST='+request.POST['protein_gapdist'])
                    if request.POST['protein_iteration'] != "":
                        option_params.append('-ITERATION='+request.POST['protein_iteration'])
                    if request.POST['protein_numiter'] != "":
                        option_params.append('-NUMITER='+request.POST['protein_numiter'])
                    if request.POST['protein_clustering'] != "":
                        option_params.append('-CLUSTERING='+request.POST['protein_clustering'])

                #parameters setting of output
                is_color = True if request.POST['output'] == 'clustal' else False
                option_params.append('-output='+request.POST['output'])
                option_params.append('-outorder='+request.POST['outorder'])

                args_list.append([path.join(program_path,'clustalw2'), '-infile='+query_filename,
                                  '-OUTFILE='+path.join(settings.MEDIA_ROOT, 'clustal', 'task', task_id, task_id+'.aln')
                                  ] + option_params)

                args_list_log = []
                args_list_log.append(['clustalw2', '-infile='+path.basename(query_filename), 
                                     '-OUTFILE='+task_id+'.aln'])

            else:
                #clustalo
                if request.POST['dealing_input'] == "yes":
                    option_params.append("--dealign")
                if request.POST['clustering_guide_tree'] != "no":
                    option_params.append("--full")
                if request.POST['clustering_guide_iter'] != "no":
                    option_params.append("--full-iter")

                if request.POST['combined_iter'] != "default":
                    option_params.append("--iterations="+request.POST['combined_iter'])
                if request.POST['max_gt_iter'] != "default":
                    option_params.append("--max-guidetree-iterations="+request.POST['max_gt_iter'])
                if request.POST['max_hmm_iter'] != "default":
                    option_params.append("--max-hmm-iterations="+request.POST['max_hmm_iter'])
                if request.POST['omega_output'] != "":
                    option_params.append("--outfmt="+request.POST['omega_output'])
                    is_color = True if request.POST['omega_output'] == 'clu' else False
                if request.POST['omega_order'] != "":
                    option_params.append("--output-order="+request.POST['omega_order'])
 
                args_list.append([path.join(program_path,'clustalo'), '--infile='+query_filename,
                                  '--guidetree-out='+path.join(settings.MEDIA_ROOT, 'clustal', 'task', task_id, task_id)+'.ph',
                                  '--outfile='+path.join(settings.MEDIA_ROOT, 'clustal', 'task', task_id, task_id)+'.aln'] 
                                  + option_params)
            
                args_list_log = []
                args_list_log.append(['clustalo', '--infile='+path.basename(query_filename),
                                      '--guidetree-out=' + task_id + '.ph', 
                                      '--outfile=' + task_id +'.aln'] + option_params)

            print(args_list)

            record = ClustalQueryRecord()
            record.task_id = task_id
            if request.user.is_authenticated():
                record.user = request.user
            record.save()

            # generate status.json for frontend status checking
            with open(query_filename, 'r') as f: # count number of query sequence by counting '>'
                qstr = f.read()
                seq_count = qstr.count('>')
                if (seq_count == 0):
                    seq_count = 1
                with open(path.join(settings.MEDIA_ROOT, 'clustal', 'task', task_id, 'status.json'), 'wb') as f:
                    json.dump({'status': 'pending', 'seq_count': seq_count, 'program':request.POST['program'], 
                               'cmd': " ".join(args_list_log[0]), 'is_color': is_color, 
                               'query_filename': path.basename(query_filename)}, f)

            run_clustal_task.delay(task_id, args_list, file_prefix)


            save_history(request.POST, task_id, query_filename)

            return redirect('clustal:retrieve', task_id)
        else:
            raise Http404

def retrieve(request, task_id='1'):
    '''
    Retrieve output of clustal tasks
    '''
    try:
        r = ClustalQueryRecord.objects.get(task_id=task_id)
        # if result is generated and not expired
        if r.result_date and (r.result_date.replace(tzinfo=None) >= (datetime.utcnow()+ timedelta(days=-7))):
            url_base_prefix = path.join(settings.MEDIA_URL, 'clustal', 'task', task_id)
            dir_base_prefix = path.join(settings.MEDIA_ROOT, 'clustal', 'task', task_id)
            url_prefix = path.join(url_base_prefix, task_id)
            dir_prefix = path.join(dir_base_prefix, task_id)

            with open(path.join(dir_base_prefix, 'status.json'), 'r') as f:
                statusdata = json.load(f)

            #10mb limitation
            out_txt = []

            aln_url = dir_prefix + '.aln'
            if path.isfile(aln_url):
                if(path.getsize(aln_url) > 1024 * 1024  * 10):
                    report = 'The Clustal reports exceed 10 Megabyte, please download it.'
                    out_txt.append(report)
                else:
                    report = ["<br>"]
                    with open(dir_prefix + '.aln', 'r') as content_file:
                        for line in content_file:
                            line = line.rstrip('\n')
                            report.append(line + "<br>")

                    out_txt.append(''.join(report).replace(' ','&nbsp;'))
            else:
                return render(request, 'clustal/results_not_existed.html',
                {
                    'title': 'Internal Error',
                    'isError': True,
                })    

            dnd_url, ph_url = None, None
            query_prefix = path.splitext(statusdata['query_filename'])[0]
            if path.isfile(path.join(dir_base_prefix,query_prefix + '.dnd')):
                dnd_url = path.join(url_base_prefix, query_prefix + '.dnd')

            ph_file = path.join(dir_base_prefix + '.ph')
            if path.isfile(ph_file):
                ph_url = url_prefix + '.ph'

            if r.result_status in set(['SUCCESS']):
                return render(
                    request,
                    'clustal/result.html', {
                        'title': 'CLUSTAL Result',
                        'aln': url_prefix + '.aln',
                        'ph': ph_url,
                        'dnd': dnd_url,
                        'status': path.join(url_base_prefix, 'status.json'),
                        'colorful': statusdata['is_color'],
                        'report': out_txt,
                        'task_id': task_id,
                    })
            else:
                return render(request, 'clustal/results_not_existed.html',
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
            if r.result_date and (r.result_date.replace(tzinfo=None) < (datetime.utcnow()+ timedelta(days=-7))):
                isExpired = True
            return render(request, 'clustal/results_not_existed.html', {
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
    '''
    function for front-end to check task status
    '''
    if request.method == 'GET':
        status_file_path = path.join(settings.MEDIA_ROOT, 'clustal', 'task', task_id, 'status.json')
        status = {'status': 'unknown'}
        if path.isfile(status_file_path):
            with open(status_file_path, 'rb') as f:
                statusdata = json.load(f)
                if statusdata['status'] == 'pending' and settings.USE_CACHE:
                    tlist = cache.get('task_list_cache', []) 
                    num_preceding = -1; 
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
from .serializers import UserClustalQueryRecordSerializer
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
        records = ClustalQueryRecord.objects.filter(user__id=user_id, result_date__gt=(localtime(now()) + timedelta(days=-7)))
        serializer = UserClustalQueryRecordSerializer(records, many=True)
        return JSONResponse(serializer.data)


def save_history(post, task_id, seq_file):
    rec = ClustalSearch()
    with open(seq_file) as f:
        rec.sequence = f.read()
  
    rec.task_id    = task_id
    rec.search_tag = post.get('tag')
    rec.enqueue_date = datetime.now()
    rec.program    = post.get('program', '')
    rec.pairwise      =  post.get('pairwise', '')
    rec.sequence_type =  post.get('sequenceType','')
    rec.pwdnamatrix   =  post.get('pwdnamatrix', '') 
    rec.dna_pwgapopen =  post.get('dna_pwgapopen') if post.get('dna_pwgapopen') != '' else 0 
    rec.dna_pwgapext  =  post.get('dna_pwgapext') if post.get('dna_pwgapext') != '' else 0 
    rec.pwmatrix      =  post.get('pwmatrix', '')
    rec.protein_pwgapopen =  post.get('protein_pwgapopen') if post.get('protein_pwgapopen') != '' else 0
    rec.protein_pwgapext  =  post.get('protein_pwgapext') if post.get('protein_pwgapext') != '' else 0 
    rec.ktuple        =  post.get('ktuple') if post.get('ktuple') != '' else 0
    rec.window        =  post.get('window') if post.get('window') != '' else 0
    rec.pairgap       =  post.get('pairgap') if post.get('pairgap') != '' else 0
    rec.topdiags      =  post.get('topdiags') if post.get('topdiags') != '' else 0
    rec.score         =  post.get('score', '')
    rec.dnamatrix     =  post.get('dnamatrix', '')
    rec.dna_gapopen   =  post.get('dna_gapopen') if post.get('dna_gapopen') != '' else 0 
    rec.dna_gapext    =  post.get('dna_gapext')  if post.get('dna_gapext') != '' else 0 
    rec.dna_gapdist   =  post.get('dna_gapdist') if post.get('dna_gapdist') != '' else 0 
    rec.dna_iteration =  post.get('dna_iteration') if post.get('dna_iteration') != '' else 0 
    rec.dna_numiter   =  post.get('dna_numiter') if post.get('dna_numiter') != '' else 0 
    rec.dna_clustering       =  post.get('dna_clustering', '')
    rec.matrix               =  post.get('matrix', '')
    rec.protein_gapopen      =  post.get('protein_gapopen') if post.get('protein_gapopen') != '' else 0 
    rec.protein_gapext       =  post.get('protein_gapext') if post.get('protein_gapext') != '' else 0 
    rec.protein_gapdist      =  post.get('protein_gapdist') if post.get('protein_gapdist') != '' else 0 
    rec.protein_iteration    =  post.get('protein_iteration') if post.get('protein_iteration') != '' else 0 
    rec.protein_numiter      =  post.get('protein_numiter') if post.get('protein_numiter') != '' else 0
    rec.protein_clustering   =  post.get('protein_clustering', '')
    rec.output               =  post.get('output', '')
    rec.outorder             =  post.get('outorder', '')
    rec.dealing_input        =  True if post.get('dealing_input') == 'yes' else False
    rec.clustering_guide_tree =  True if post.get('clustering_guide_tree') == 'yes' else False
    rec.clustering_guide_iter =  True if post.get('clustering_guide_iter') == 'yes' else False
    rec.combined_iter         =  post.get('combined_iter', '')
    rec.max_gt_iter           =  post.get('max_gt_iter', '')
    rec.max_hmm_iter          =  post.get('max_hmm_iter', '')
    rec.omega_output          =  post.get('omega_output', '')
    rec.omega_order           =  post.get('omega_order', '')
    rec.save() 
