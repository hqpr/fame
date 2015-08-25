# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0026_video_plays'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='plays',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='plays',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
