# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0034_competition_competition_tagline'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionentryrating',
            name='description',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
