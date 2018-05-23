from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from blast.models import BlastSearch
from hmmer.models import HmmerSearch
from clustal.models import ClustalSearch
from misc.logger import i5kLogger
from datetime import datetime
import json

dash = i5kLogger()


def dashboard(request):
    search_list = []
    print 'Method: %s' % request.method
    print 'Path: %s' % request.path # can be in two forms: /dashboard or /webapp/dashboard (also can be ended with /)
    if request.path.endswith('/'):
        relative_path = request.path.rstrip('/')
    else:
        relative_path = request.path
    relative_path = relative_path.split('/')[-1]
    if request.method == 'GET':
        id_num = 0
        if relative_path.startswith('dashboard') or relative_path.startswith('home'):
            print "GET: %s" % request.GET
            if 'search_id' in request.GET:
                if request.GET['app'] == 'blast':
                    search = BlastSearch.objects.all().filter(search_tag=request.GET['search_id'])
                elif request.GET['app'] == 'hmmer':
                    search = HmmerSearch.objects.all().filter(search_tag=request.GET['search_id'])
                elif request.GET['app'] == 'clustal':
                    search = ClustalSearch.objects.all().filter(search_tag=request.GET['search_id'])
                if not search:
                    print 'No search FOUND'
                    return render(request, 'dashboard/index.html')
                search = search[0]
                print 'search found: %s %s' % (search.search_tag, search.task_id)
            if 'searchagain' in request.GET:
                print 'SEARCHAGAIN'
                if request.GET['app'] == 'blast':
                    return redirect(reverse('blast:retrieve', kwargs={'task_id': search.task_id}))
                elif request.GET['app'] == 'hmmer':
                    return redirect(reverse('hmmer:retrieve', kwargs={'task_id': search.task_id}))
                elif request.GET['app'] == 'clustal':
                    return redirect(reverse('clustal:retrieve', kwargs={'task_id': search.task_id}))
            elif 'editsearch' in request.GET:
                print 'EDITSEARCH'
                if request.GET['app'] == 'blast':
                    return redirect(reverse('blast:create') + '?search_id=%s' % search.search_tag)
                elif request.GET['app'] == 'hmmer':
                    return redirect(reverse('hmmer:create') + '?search_id=%s' % search.search_tag)
                elif request.GET['app'] == 'clustal':
                    return redirect(reverse('clustal:create') + '?search_id=%s' % search.search_tag)
            else:
                return render(request, 'dashboard/index.html')
        elif relative_path == 'blast_hist':
            search_list = []
            if request.user.is_authenticated():
                for obj in BlastSearch.objects.filter(user=request.user.id):
                    search_dict = {}
                    id_num += 1
                    orgs = json.loads(obj.organisms)
                    orglist = orgs.split()
                    forgs = orglist[0]
                    seq = (obj.sequence[:20] + '..') if len(obj.sequence) > 20 else obj.sequence
                    date_str = obj.enqueue_date.strftime('%b %d %H:%M:%S')
                    search_dict['search_head']     = '%s  -  %s  -  %s  -  %s' % (obj.search_tag, date_str, obj.program, forgs)
                    search_dict['id_str']          = 'collapsible' + str(id_num)
                    search_dict['task_id']         = obj.task_id
                    search_dict['search_tag']      = obj.search_tag
                    search_dict['soft_masking']    = obj.soft_masking
                    search_dict['enqueue_date']    = obj.enqueue_date
                    search_dict['low_complexity']  = obj.low_complexity
                    search_dict['penalty']         = obj.penalty
                    search_dict['evalue']          = obj.evalue
                    search_dict['gapopen']         = obj.gapopen
                    search_dict['strand']          = obj.strand
                    search_dict['program']         = obj.program
                    search_dict['reward']          = obj.reward
                    search_dict['gapextend']       = obj.gapextend
                    search_dict['word_size']       = obj.word_size
                    search_dict['max_target_seqs'] = obj.max_target_seqs
                    search_dict['sequence']        = seq
                    search_dict['organisms']       = orgs
                    search_list.append(search_dict)
            return render(request, 'dashboard/blast_hist.html', { 'search_list': search_list})
        elif relative_path == 'hmmer_hist':
            if request.user.is_authenticated():
                for obj in HmmerSearch.objects.filter(user=request.user.id):
                    search_dict = {}
                    id_num += 1
                    orgs = json.loads(obj.organisms)
                    orglist = orgs.split()
                    forgs = orglist[0]
                    seq = (obj.sequence[:20] + '..') if len(obj.sequence) > 20 else obj.sequence
                    date_str = obj.enqueue_date.strftime('%b %d %H:%M:%S')
                    search_dict['search_head']     = '%s  -  %s  -  %s  -  %s' % (obj.search_tag, date_str, obj.program, forgs)
                    search_dict['id_str']          = 'collapsible' + str(id_num)
                    search_dict['task_id']         = obj.task_id
                    search_dict['search_tag']      = obj.search_tag
                    search_dict['enqueue_date']    = obj.enqueue_date
                    search_dict['program']         = obj.program
                    search_dict['sequence']        = seq
                    search_dict['organisms']       = orgs
                    search_list.append(search_dict)
            return render(request, 'dashboard/hmmer_hist.html', { 'search_list': search_list})
        elif relative_path == 'clustal_hist':
            search_list = []
            if request.user.is_authenticated():
                for obj in ClustalSearch.objects.filter(user=request.user.id):
                    search_dict = {}
                    id_num += 1
                    seq = (obj.sequence[:20] + '..') if len(obj.sequence) > 20 else obj.sequence
                    date_str = obj.enqueue_date.strftime('%b %d %H:%M:%S')
                    search_dict['search_head']     = '%s  -  %s  -  %s' % (obj.search_tag, date_str, obj.program)
                    search_dict['id_str']          = 'collapsible' + str(id_num)
                    search_dict['task_id']         = obj.task_id
                    search_dict['search_tag']      = obj.search_tag
                    search_dict['enqueue_date']    = obj.enqueue_date
                    search_dict['program']         = obj.program
                    search_dict['sequence']        = obj.sequence
                    search_list.append(search_dict)
            return render(request, 'dashboard/clustal_hist.html', { 'search_list': search_list})

    elif request.method == 'POST':
        return render(request, 'dashboard/index.html', { 'year': datetime.now().year, 'title': 'Dashboard', })
