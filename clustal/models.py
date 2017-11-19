from django.db import models
from django.contrib.auth.models import User

class ClustalQueryRecord(models.Model):
    task_id = models.CharField(max_length=32, primary_key=True)
    enqueue_date = models.DateTimeField(auto_now_add=True)
    dequeue_date = models.DateTimeField(null=True)
    result_date = models.DateTimeField(null=True)
    result_status = models.CharField(max_length=32, default='WAITING')
    user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        verbose_name = 'Clustal result'


class ClustalSearch(models.Model):
    #
    #  Holds search parameters.
    #
    task_id               = models.CharField(max_length=32, primary_key=True)
    search_tag      = models.CharField(max_length=64) 
    create_date           = models.DateTimeField(auto_now_add=True)
    user                  = models.ForeignKey(User, null=True, blank=True)
    #sequence_type
    program               = models.CharField(max_length=32)
    pairwise              = models.CharField(max_length=10)
    pwdnamatrix           = models.CharField(max_length=10)
    dna_pwgapopen         = models.IntegerField()
    dna_pwgapext          = models.IntegerField()
    pwmatrix              = models.CharField(max_length=10)
    protein_pwgapopen     = models.IntegerField()
    protein_pwgapext      = models.IntegerField()
    ktuple                = models.IntegerField()
    window                = models.IntegerField()
    pairgap               = models.IntegerField()
    topdiags              = models.IntegerField()
    score                 = models.CharField(max_length=10)
    dnamatrix             = models.CharField(max_length=10)
    dna_gapopen           = models.IntegerField()
    dna_gapext            = models.IntegerField()
    dna_gapdist           = models.IntegerField()
    dna_iteration         = models.IntegerField()
    dna_numiter           = models.IntegerField()
    dna_clustering        = models.CharField(max_length=10)
    matrix                = models.CharField(max_length=10)
    protein_gapopen       = models.IntegerField()
    protein_gapext        = models.IntegerField()
    protein_gapdist       = models.IntegerField()
    protein_iteration     = models.IntegerField()
    protein_numiter       = models.IntegerField()
    protein_clustering    = models.CharField(max_length=10)
    output                = models.CharField(max_length=10)
    outorder              = models.CharField(max_length=10)
    #OMEGA
    dealing_input         = models.BooleanField()
    clustering_guide_tree = models.BooleanField()
    clustering_guide_iter = models.BooleanField()
    combined_iter         = models.CharField(max_length=10)
    max_gt_iter           = models.CharField(max_length=10)
    max_hmm_iter          = models.CharField(max_length=10)
    omega_output          = models.CharField(max_length=10)
    omega_order           = models.CharField(max_length=10)





# Create your models here.
