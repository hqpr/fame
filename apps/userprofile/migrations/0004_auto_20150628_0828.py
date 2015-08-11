# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20150626_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='account_type',
            field=models.CharField(max_length=100, choices=[(b'1', b'Artist'), (b'2', b'Music Explorer'), (b'3', b'Music Industry')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2015, 6, 28, 8, 28, 43, 939012)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 28, 8, 28, 43, 944440), editable=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 28, 8, 28, 43, 944481)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'avatars', blank=True),
        ),
    ]
