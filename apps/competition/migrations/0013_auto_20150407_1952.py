# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0012_auto_20150407_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionstage',
            name='ordering',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='competition',
            name='competition_page_image',
            field=models.ImageField(upload_to=b'%y/%m/%d', null=True, verbose_name=b'Competition Image', blank=True),
        ),
    ]
