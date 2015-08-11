# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20150626_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2015, 6, 26, 7, 36, 52, 752394)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 26, 7, 36, 52, 757324), editable=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 26, 7, 36, 52, 757383)),
        ),
    ]
