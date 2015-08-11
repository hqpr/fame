# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0019_competitionentryaudio_competitionentryimage_competitionentryvideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionentry',
            name='knocked_out',
            field=models.BooleanField(default=False),
        ),
    ]
