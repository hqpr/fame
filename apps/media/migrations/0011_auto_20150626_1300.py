# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0010_auto_20150626_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoplaylist',
            name='added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='videoplaylist',
            name='artist',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='videoplaylist',
            name='description',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='videoplaylist',
            name='genre',
            field=models.ForeignKey(default=1, to='media.Genre'),
        ),
        migrations.AddField(
            model_name='videoplaylist',
            name='privacy',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
