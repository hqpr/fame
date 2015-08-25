# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0031_auto_20150414_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitionchart',
            name='entry',
            field=models.ForeignKey(to='competition.CompetitionEntry', unique=True),
        ),
    ]
