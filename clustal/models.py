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


class ClustalSearch(modeld.Model)
    #
    #  Holds search parameters.
    #
    task_id               = models.CharField(max_length=32, primary_key=True)
    create_date           = models.DateTimeField(auto_now_add=True)
    user                  = models.ForeignKey(User, null=True, blank=True)
    program               = models.CharField(max_length=32)
    pairwise              = models.CharField(max_length=32)
    pwdnamatrix           = models.CharField(max_length=32)
    dna-pwgapopen         = models.CharField(max_length=32)
    dna-pwgapext          = models.CharField(max_length=32)
    pwmatrix              = models.CharField(max_length=32)
    protein-pwgapopen     = models.CharField(max_length=32)
    protein-pwgapext      = models.CharField(max_length=32)
    ktuple                = models.CharField(max_length=32)
    window                = models.CharField(max_length=32)
    pairgap               = models.CharField(max_length=32)
    topdiags              = models.CharField(max_length=32)
    score                 = models.CharField(max_length=32)
    dnamatrix             = models.CharField(max_length=32)
    dna-gapopen           = models.CharField(max_length=32)
    dna-gapext            = models.CharField(max_length=32)
    dna-gapdist           = models.CharField(max_length=32)
    dna-iteration         = models.CharField(max_length=32)
    dna-numiter           = models.CharField(max_length=32)
    dna-clustering        = models.CharField(max_length=32)
    matrix                = models.CharField(max_length=32)
    protein-gapopen       = models.CharField(max_length=32)
    protein-gapext        = models.CharField(max_length=32)
    protein-gapdist       = models.CharField(max_length=32)
    protein-iteration     = models.CharField(max_length=32)
    protein-numiter       = models.CharField(max_length=32)
    protein-clustering    = models.CharField(max_length=32)
    output                = models.CharField(max_length=32)
    outorder              = models.CharField(max_length=32)
    dealing_input         = models.CharField(max_length=32)
    clustering_guide_tree = models.CharField(max_length=32)
    clustering_guide_iter = models.CharField(max_length=32)
    combined_iter         = models.CharField(max_length=32)
    max_gt_iter           = models.CharField(max_length=32)
    max_hmm_iter          = models.CharField(max_length=32)
    omega_output          = models.CharField(max_length=32)
    omega_order           = models.CharField(max_length=32)







# Create your models here.
