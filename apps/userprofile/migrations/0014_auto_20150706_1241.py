# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0013_auto_20150706_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='halloffameartists',
            name='type',
            field=models.CharField(default=b'winners', max_length=10, choices=[(b'winners', b'Winners'), (b'patrons', b'Patrons'), (b'sponsors', b'Sponsors')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 6, 12, 41, 6, 781686)),
        ),
    ]
