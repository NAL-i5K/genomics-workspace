# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blast', '0008_auto_20180130_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='JbrowseSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text=b'The URL to Jbrowse using this reference', unique=True, verbose_name=b'Jbrowse URL')),
                ('blast_db', models.OneToOneField(verbose_name=b'reference', to='blast.BlastDb', help_text=b'The BLAST database used as the reference in Jbrowse')),
            ],
        ),
    ]
