# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0006_auto_20150622_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
