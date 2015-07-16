# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0022_auto_20150710_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='background_image',
            field=models.ImageField(null=True, upload_to=b'backgrounds/%y/%m/%d', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'avatars/%y/%m/%d', blank=True),
        ),
    ]
