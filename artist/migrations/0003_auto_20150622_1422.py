# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0002_music'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='music',
            name='user',
        ),
        migrations.DeleteModel(
            name='Music',
        ),
    ]
