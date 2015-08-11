# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0024_usersocial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='about',
            field=models.TextField(null=True, blank=True),
        ),
    ]
