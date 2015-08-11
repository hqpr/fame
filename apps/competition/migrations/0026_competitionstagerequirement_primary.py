# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0025_auto_20150410_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionstagerequirement',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]
