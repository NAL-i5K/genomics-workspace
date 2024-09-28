# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
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
