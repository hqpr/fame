# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0012_videoplaylist_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='artist',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
        ),
    ]
