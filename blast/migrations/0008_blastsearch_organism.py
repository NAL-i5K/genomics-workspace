# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blast', '0007_auto_20171218_1649'),
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
        migrations.CreateModel(
            name='Organism',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(help_text=b'Scientific or common name', unique=True, max_length=200)),
                ('short_name', models.CharField(help_text=b'This is used for file names and variable names in code', unique=True, max_length=20)),
                ('description', models.TextField(blank=True)),
                ('tax_id', models.PositiveIntegerField(help_text=b'This is passed into makeblast', null=True, verbose_name=b'NCBI Taxonomy ID', blank=True)),
            ],
        ),
    ]
