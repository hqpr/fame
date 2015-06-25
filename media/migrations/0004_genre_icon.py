# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_auto_20150410_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='icon',
            field=models.ImageField(default='', upload_to=b'genre/%y/%m/%d'),
            preserve_default=False,
        ),
    ]
