# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0030_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='description_it',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='genre_it',
            field=models.ForeignKey(blank=True, to='media.Genre', null=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='name_it',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='audio',
            name='length',
            field=models.CharField(default=0, max_length=255, null=True, blank=True),
        ),
    ]
