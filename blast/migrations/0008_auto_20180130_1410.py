# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blast', '0007_auto_20180104_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jbrowsesetting',
            name='blast_db',
        ),
        migrations.DeleteModel(
            name='JbrowseSetting',
        ),
    ]
