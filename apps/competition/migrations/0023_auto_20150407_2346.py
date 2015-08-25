# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0022_auto_20150407_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionjudge',
            name='carousel_image',
            field=models.ImageField(default='', upload_to=b'judges/carousel/%y/%m/%d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competitionjudge',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competitionjudge',
            name='ordering',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competitionjudge',
            name='thumbnail_image',
            field=models.ImageField(default='', upload_to=b'judges/thumbs/%y/%m/%d'),
            preserve_default=False,
        ),
    ]
