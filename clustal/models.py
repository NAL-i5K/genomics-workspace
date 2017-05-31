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
    create_date           = models.DateTimeField(auto_now_add=True)
    user                  = models.CharField(max_length=40, default="NOUSER")
    search_tag            = models.CharField(max_length=64, default="NOTAG")
    program               = models.CharField(max_length=32)
    sequence              = models.TextField()
    sequenceType          = models.CharField(max_length=32, default="")
    pairwise              = models.CharField(max_length=32)
    PWDNAMATRIX           = models.CharField(max_length=32)
    dna_PWGAPOPEN         = models.CharField(max_length=32)
    dna_PWGAPEXT          = models.CharField(max_length=32)
    PWMATRIX              = models.CharField(max_length=32)
    protein_PWGAPOPEN     = models.CharField(max_length=32)
    protein_PWGAPEXT      = models.CharField(max_length=32)
    KTUPLE                = models.CharField(max_length=32)
    WINDOW                = models.CharField(max_length=32)
    PAIRGAP               = models.CharField(max_length=32)
    TOPDIAGS              = models.CharField(max_length=32)
    SCORE                 = models.CharField(max_length=32)
    DNAMATRIX             = models.CharField(max_length=32)
    dna_GAPOPEN           = models.CharField(max_length=32)
    dna_GAPEXT            = models.CharField(max_length=32)
    dna_GAPDIST           = models.CharField(max_length=32)
    dna_ITERATION         = models.CharField(max_length=32)
    dna_NUMITER           = models.CharField(max_length=32)
    dna_CLUSTERING        = models.CharField(max_length=32)
    MATRIX                = models.CharField(max_length=32)
    protein_GAPOPEN       = models.CharField(max_length=32)
    protein_GAPEXT        = models.CharField(max_length=32)
    protein_GAPDIST       = models.CharField(max_length=32)
    protein_ITERATION     = models.CharField(max_length=32)
    protein_NUMITER       = models.CharField(max_length=32)
    protein_CLUSTERING    = models.CharField(max_length=32)
    OUTPUT                = models.CharField(max_length=32)
    OUTORDER              = models.CharField(max_length=32)
    dealing_input         = models.CharField(max_length=32)
    clustering_guide_tree = models.CharField(max_length=32)
    clustering_guide_iter = models.CharField(max_length=32)
    combined_iter         = models.CharField(max_length=32)
    max_gt_iter           = models.CharField(max_length=32)
    max_hmm_iter          = models.CharField(max_length=32)
    omega_output          = models.CharField(max_length=32)
    omega_order           = models.CharField(max_length=32)







# Create your models here.
