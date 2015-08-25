# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0021_auto_20150407_2326'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='competitionjudge',
            unique_together=set([('competition', 'judge')]),
        ),
    ]
