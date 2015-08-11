# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0011_auto_20150626_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoplaylist',
            name='cover',
            field=models.ImageField(null=True, upload_to=b'playlists/%y/%m/%d', blank=True),
        ),
    ]
