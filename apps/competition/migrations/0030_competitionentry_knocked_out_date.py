# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0029_auto_20150413_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionentry',
            name='knocked_out_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
