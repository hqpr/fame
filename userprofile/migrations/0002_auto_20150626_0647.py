# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 26, 6, 47, 29, 496289), editable=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 26, 6, 47, 29, 496347)),
        ),
    ]
