# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0024_auto_20150707_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='plays',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
