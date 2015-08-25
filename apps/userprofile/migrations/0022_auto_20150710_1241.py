# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0021_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(default=b''),
        ),
    ]
