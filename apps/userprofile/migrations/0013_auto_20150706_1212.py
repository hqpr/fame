# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0012_auto_20150706_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='halloffameartists',
            name='user',
            field=models.OneToOneField(to='userprofile.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 6, 12, 12, 33, 332507)),
        ),
    ]
