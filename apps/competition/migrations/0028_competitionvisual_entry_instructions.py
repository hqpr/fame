# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0027_competitionstage_new_entries_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionvisual',
            name='entry_instructions',
            field=models.TextField(null=True, blank=True),
        ),
    ]
