# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0034_auto_20150728_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='soundcloud_track_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
