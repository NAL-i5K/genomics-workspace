# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clustal', '0002_auto_20171218_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClustalSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.CharField(max_length=50, null=True)),
                ('search_tag', models.CharField(max_length=64)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('enqueue_date', models.DateTimeField()),
                ('sequence', models.TextField(null=True)),
                ('program', models.CharField(max_length=32)),
                ('pairwise', models.CharField(max_length=10, blank=True)),
                ('sequence_type', models.CharField(max_length=10, blank=True)),
                ('pwdnamatrix', models.CharField(max_length=10, blank=True)),
                ('dna_pwgapopen', models.IntegerField()),
                ('dna_pwgapext', models.IntegerField()),
                ('pwmatrix', models.CharField(max_length=10, blank=True)),
                ('protein_pwgapopen', models.IntegerField()),
                ('protein_pwgapext', models.IntegerField()),
                ('ktuple', models.IntegerField()),
                ('window', models.IntegerField()),
                ('pairgap', models.IntegerField()),
                ('topdiags', models.IntegerField()),
                ('score', models.CharField(max_length=10, blank=True)),
                ('dnamatrix', models.CharField(max_length=10, blank=True)),
                ('dna_gapopen', models.IntegerField()),
                ('dna_gapext', models.IntegerField()),
                ('dna_gapdist', models.IntegerField()),
                ('dna_iteration', models.CharField(max_length=16, blank=True)),
                ('dna_numiter', models.IntegerField()),
                ('dna_clustering', models.CharField(max_length=16, blank=True)),
                ('matrix', models.CharField(max_length=16, blank=True)),
                ('protein_gapopen', models.IntegerField()),
                ('protein_gapext', models.IntegerField()),
                ('protein_gapdist', models.IntegerField()),
                ('protein_iteration', models.CharField(max_length=16, blank=True)),
                ('protein_numiter', models.IntegerField()),
                ('protein_clustering', models.CharField(max_length=16, blank=True)),
                ('output', models.CharField(max_length=16, blank=True)),
                ('outorder', models.CharField(max_length=16, blank=True)),
                ('dealing_input', models.BooleanField()),
                ('clustering_guide_tree', models.BooleanField()),
                ('clustering_guide_iter', models.BooleanField()),
                ('combined_iter', models.CharField(max_length=16, blank=True)),
                ('max_gt_iter', models.CharField(max_length=16, blank=True)),
                ('max_hmm_iter', models.CharField(max_length=16, blank=True)),
                ('omega_output', models.CharField(max_length=16, blank=True)),
                ('omega_order', models.CharField(max_length=16, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
