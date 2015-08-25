# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150706_1539'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcategory',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='blogtag',
            options={'verbose_name_plural': 'Tags'},
        ),
        migrations.AddField(
            model_name='blogitemcomment',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blogitemcomment',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 6, 16, 18, 2, 79476, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
