# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0019_audiocomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiocomment',
            name='time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='audiocomment',
            name='time_specific',
            field=models.BooleanField(default=False),
        ),
    ]
