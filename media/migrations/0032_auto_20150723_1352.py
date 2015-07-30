# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0031_auto_20150723_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='description_en',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='genre_en',
            field=models.ForeignKey(blank=True, to='media.Genre', null=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='name_en',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
