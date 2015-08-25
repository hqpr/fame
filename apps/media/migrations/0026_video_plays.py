# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0025_audio_plays'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='plays',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
