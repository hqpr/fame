# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0028_auto_20150721_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='length',
            field=models.CharField(default=b'0', max_length=255, null=True, blank=True),
        ),
    ]
