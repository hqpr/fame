# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogitem_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogitem',
            name='publish_date',
            field=models.DateTimeField(),
        ),
    ]
