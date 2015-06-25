# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0004_genre_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='uid',
            field=models.CharField(max_length=11, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='image',
            name='uid',
            field=models.CharField(max_length=11, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='uid',
            field=models.CharField(max_length=11, unique=True, null=True, blank=True),
        ),
    ]
