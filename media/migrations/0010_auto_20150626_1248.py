# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0009_auto_20150626_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='genre',
            field=models.ForeignKey(blank=True, to='media.Genre', null=True),
        ),
    ]
