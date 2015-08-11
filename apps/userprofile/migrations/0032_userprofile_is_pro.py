# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0031_usergenre'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_pro',
            field=models.BooleanField(default=False),
        ),
    ]
