# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 15, 31, 44, 87612, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
