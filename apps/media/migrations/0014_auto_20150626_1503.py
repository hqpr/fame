# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0013_audio_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='audio',
            field=models.FileField(default=b'default.mp3', upload_to=b'audios/%y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='cover',
            field=models.FileField(null=True, upload_to=b'audios/covers/%y/%m/%d', blank=True),
        ),
    ]
