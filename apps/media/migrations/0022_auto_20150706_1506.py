# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0021_auto_20150706_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoplaylist',
            name='cover',
            field=models.ImageField(null=True, upload_to=b'video-playlists/%y/%m/%d', blank=True),
        ),
    ]
