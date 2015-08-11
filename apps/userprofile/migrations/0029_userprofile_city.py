# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0028_userprofile_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
