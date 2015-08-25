# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0032_auto_20150723_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='artist_en',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='artist_it',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
        ),
    ]
