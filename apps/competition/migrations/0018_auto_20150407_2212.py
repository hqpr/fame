# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0017_auto_20150407_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionentry',
            name='final_points',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competitionentry',
            name='final_position',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
