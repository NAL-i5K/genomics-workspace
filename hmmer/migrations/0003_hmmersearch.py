# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hmmer', '0002_auto_20171218_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='HmmerSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.CharField(max_length=50, null=True)),
                ('search_tag', models.CharField(max_length=64)),
                ('enqueue_date', models.DateTimeField()),
                ('sequence', models.TextField(null=True)),
                ('program', models.CharField(max_length=10)),
                ('cut_off', models.CharField(max_length=10)),
                ('significane_seq', models.DecimalField(max_digits=10, decimal_places=5)),
                ('significane_hit', models.DecimalField(max_digits=10, decimal_places=5)),
                ('report_seq', models.DecimalField(max_digits=10, decimal_places=5)),
                ('report_hit', models.DecimalField(max_digits=10, decimal_places=5)),
                ('organisms', models.TextField(null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
