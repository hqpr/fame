# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0032_userprofile_is_pro'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='artist_types',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='genres',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='influences',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
