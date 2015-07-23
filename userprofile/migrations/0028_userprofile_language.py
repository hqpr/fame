# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0027_userinfluencer_usertypes'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='language',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
