# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blast', '0006_auto_20150410_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlastSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.CharField(max_length=50, null=True)),
                ('search_tag', models.CharField(max_length=64)),
                ('enqueue_date', models.DateTimeField()),
                ('sequence', models.TextField(null=True)),
                ('program', models.CharField(max_length=32)),
                ('soft_masking', models.BooleanField()),
                ('low_complexity', models.BooleanField()),
                ('penalty', models.IntegerField()),
                ('evalue', models.DecimalField(max_digits=10, decimal_places=5)),
                ('gapopen', models.IntegerField()),
                ('strand', models.CharField(max_length=10)),
                ('gapextend', models.IntegerField()),
                ('word_size', models.IntegerField()),
                ('reward', models.IntegerField()),
                ('max_target_seqs', models.IntegerField()),
                ('organisms', models.TextField(null=True)),
                ('matrix', models.CharField(max_length=10, null=True)),
                ('threshold', models.IntegerField(null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='blastdb',
            name='fasta_file',
            field=filebrowser.fields.FileBrowseField(max_length=200, verbose_name=b'FASTA file path'),
        ),
        migrations.AlterField(
            model_name='blastdb',
            name='organism',
            field=models.ForeignKey(to='app.Organism'),
        ),
    ]
