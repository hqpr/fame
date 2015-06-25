# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0002_auto_20150407_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='competition_page_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='competition_page_image',
            field=models.ImageField(default='', upload_to=b'%y/%m/%d'),
            preserve_default=False,
        ),
    ]
