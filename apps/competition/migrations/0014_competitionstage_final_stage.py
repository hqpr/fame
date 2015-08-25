# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0013_auto_20150407_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionstage',
            name='final_stage',
            field=models.BooleanField(default=False),
        ),
    ]
