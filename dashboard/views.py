'''
    Dashboard views.py
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from blast.models import BlastSearch
from clustal.models import ClustalSearch
from misc.logger import i5kLogger
from django.http import Http404
from datetime import datetime
import misc.fileline as src
import logging
import json
import sys
import os

dash = i5kLogger()

def dashboard(request):
    search_list = []
    print 'Method: %s' % request.method
    print 'Path: %s' % request.path
    if request.method == 'GET':
        id_num = 0
        if request.path == '/dashboard' or request.path == '/home':
            print "GET: %s" % request.GET
            if 'search_id' in request.GET:
                search = BlastSearch.objects.all().filter(search_tag=request.GET['search_id'])
                if not search:
                    print 'No search FOUND'
                    return render(request, 'dashboard/index.html')
                search = search[0]
                print 'search found: %s %s' % (search.search_tag, search.task_id)
            if 'searchagain' in request.GET:
                print 'SEARCHAGAIN'
                return redirect('/blast/%s' % search.task_id)
            elif 'editsearch' in request.GET:
                print 'EDITSEARCH'
                return redirect('/blast?search_id=%s' % search.search_tag)
            else:
                return render(request, 'dashboard/index.html')
        if request.path == '/blast_hist':
            search_list = []
            for obj in BlastSearch.objects.all():
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

        if request.path == '/clustal_hist':
            #
            #  Clustal history.
            #
            search_list = []
            for obj in ClustalSearch.objects.all():
                id_num += 1
                search_dict = {}
                date_str                             = obj.create_date.strftime('%b %d %H:%M:%S')
                search_dict['search_head']           = '%s  -  %s  -  %s' % (obj.search_tag, date_str, obj.program)
                search_dict['id_str']                = 'collapsible' + str(id_num)
                search_dict['task_id']               = obj.task_id
                search_dict['sequence']              = obj.sequence
                search_dict['create_date']           = obj.create_date
                search_dict['user']                  = obj.user
                search_dict['program']               = obj.program
                search_dict['sequence']              = obj.sequence
                search_dict['pairwise']              = obj.pairwise
                search_dict['PWDNAMATRIX']           = obj.PWDNAMATRIX
                search_dict['dna_PWGAPOPEN']         = obj.dna_PWGAPOPEN
                search_dict['dna_PWGAPEXT']          = obj.dna_PWGAPEXT
                search_dict['PWMATRIX']              = obj.PWMATRIX
                search_dict['protein_PWGAPOPEN']     = obj.protein_PWGAPOPEN
                search_dict['protein_PWGAPEXT']      = obj.protein_PWGAPEXT
                search_dict['KTUPLE']                = obj.KTUPLE
                search_dict['WINDOW']                = obj.WINDOW
                search_dict['PAIRGAP']               = obj.PAIRGAP
                search_dict['TOPDIAGS']              = obj.TOPDIAGS
                search_dict['SCORE']                 = obj.SCORE
                search_dict['DNAMATRIX']             = obj.DNAMATRIX
                search_dict['dna_GAPOPEN']           = obj.dna_GAPOPEN
                search_dict['dna_GAPEXT']            = obj.dna_GAPEXT
                search_dict['dna_GAPDIST']           = obj.dna_GAPDIST
                search_dict['dna_ITERATION']         = obj.dna_ITERATION
                search_dict['dna_NUMITER']           = obj.dna_NUMITER
                search_dict['dna_CLUSTERING']        = obj.dna_CLUSTERING
                search_dict['MATRIX']                = obj.MATRIX
                search_dict['protein_GAPOPEN']       = obj.protein_GAPOPEN
                search_dict['protein_GAPEXT']        = obj.protein_GAPEXT
                search_dict['protein_GAPDIST']       = obj.protein_GAPDIST
                search_dict['protein_ITERATION']     = obj.protein_ITERATION
                search_dict['protein_NUMITER']       = obj.protein_NUMITER
                search_dict['protein_CLUSTERING']    = obj.protein_CLUSTERING
                search_dict['OUTPUT']                = obj.OUTPUT
                search_dict['OUTORDER']              = obj.OUTORDER
                search_dict['dealing_input']         = obj.dealing_input
                search_dict['clustering_guide_tree'] = obj.clustering_guide_tree
                search_dict['clustering_guide_iter'] = obj.clustering_guide_iter
                search_dict['combined_iter']         = obj.combined_iter
                search_dict['max_gt_iter']           = obj.max_gt_iter
                search_dict['max_hmm_iter']          = obj.max_hmm_iter
                search_dict['omega_output']          = obj.omega_output
                search_list.append(search_dict)
            return render(request, 'dashboard/clustal_hist.html', { 'search_list': search_list })

    elif request.method == 'POST':
        return render(request, 'dashboard/index.html', { 'year': datetime.now().year, 'title': 'Dashboard', })
