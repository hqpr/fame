# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150706_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategory',
            name='slug',
            field=models.CharField(max_length=255, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='blogtag',
            name='slug',
            field=models.CharField(max_length=255, unique=True, null=True, blank=True),
        ),
    ]
