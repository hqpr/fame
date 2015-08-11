# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0033_competitionentry_uid_string'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='competition_tagline',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Tag Line', blank=True),
        ),
    ]
