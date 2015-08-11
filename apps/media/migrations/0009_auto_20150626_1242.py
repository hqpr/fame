# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0008_videoplaylist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='genre',
            field=models.ForeignKey(to='apps.media.Genre'),
        ),
    ]
