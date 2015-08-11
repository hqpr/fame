# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0010_auto_20150703_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 5, 10, 58, 11, 149548)),
        ),
    ]
