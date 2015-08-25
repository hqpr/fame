# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0029_userprofile_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='account_type',
            field=models.CharField(max_length=100, choices=[(b'1', b'Artist'), (b'2', b'Muser'), (b'3', b'Music Industry')]),
        ),
    ]
