# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0030_competitionentry_knocked_out_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='competitionchart',
            name='final',
            field=models.BooleanField(default=False),
        ),
    ]
