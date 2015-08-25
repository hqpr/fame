# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_auto_20150407_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='competition_page_description',
            field=models.TextField(null=True, verbose_name=b'Competition Description', blank=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='competition_page_image',
            field=models.ImageField(upload_to=b'%y/%m/%d', verbose_name=b'Competition Image'),
        ),
    ]
