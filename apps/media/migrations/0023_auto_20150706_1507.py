# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0022_auto_20150706_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audioplaylist',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='audioplaylist',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='audioplaylist',
            name='privacy',
        ),
    ]
