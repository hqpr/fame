# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0026_competitionstagerequirement_primary'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionstage',
            name='new_entries_open',
            field=models.BooleanField(default=False),
        ),
    ]
