# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blast', '0006_auto_20150410_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blastdb',
            name='fasta_file',
            field=filebrowser.fields.FileBrowseField(max_length=200, verbose_name='FASTA file path'),
        ),
        migrations.AlterField(
            model_name='blastdb',
            name='organism',
            field=models.ForeignKey(to='app.Organism'),
        ),
    ]
