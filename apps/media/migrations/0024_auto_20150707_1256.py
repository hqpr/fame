# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0023_auto_20150706_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoplaylist',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='videoplaylist',
            name='user',
        ),
        migrations.RemoveField(
            model_name='videoplaylist',
            name='videos',
        ),
        migrations.DeleteModel(
            name='VideoPlaylist',
        ),
    ]
