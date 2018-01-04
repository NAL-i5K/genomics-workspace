# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hmmer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hmmerqueryrecord',
            options={'verbose_name': 'Hmmer result'},
        ),
        migrations.AlterField(
            model_name='hmmerdb',
            name='is_shown',
            field=models.BooleanField(default=None, help_text=b'Display this database in the HMMER submit form'),
        ),
        migrations.AlterField(
            model_name='hmmerdb',
            name='organism',
            field=models.ForeignKey(default=0, to='app.Organism'),
        ),
        migrations.AlterField(
            model_name='hmmerdb',
            name='title',
            field=models.CharField(default=b'', unique=True, max_length=200),
        ),
    ]
