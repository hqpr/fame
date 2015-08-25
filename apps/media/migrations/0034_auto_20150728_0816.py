# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0033_auto_20150723_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiocomment',
            name='time',
            field=models.CharField(max_length=255),
        ),
    ]
