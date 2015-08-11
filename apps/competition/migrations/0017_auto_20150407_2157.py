# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0016_competitionentry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competitionentry',
            options={'verbose_name_plural': 'Competition Entries'},
        ),
        migrations.AlterModelTable(
            name='competitionentry',
            table='competition_entries',
        ),
    ]
