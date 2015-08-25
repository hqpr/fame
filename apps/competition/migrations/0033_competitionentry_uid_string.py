# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0032_auto_20150414_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionentry',
            name='uid_string',
            field=models.CharField(max_length=11, unique=True, null=True, blank=True),
        ),
    ]
