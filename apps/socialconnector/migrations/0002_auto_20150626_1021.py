# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialconnector', '0001_initial'),
    ]

    operations = [
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
