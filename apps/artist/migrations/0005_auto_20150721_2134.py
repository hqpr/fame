# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0004_userconnections'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userconnections',
            unique_together=set([('user', 'connection')]),
        ),
    ]
