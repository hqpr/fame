# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0027_auto_20150720_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='privacy',
            field=models.CharField(default=b'public', max_length=255, choices=[(b'private', b'Private'), (b'public', b'Public')]),
        ),
        migrations.AlterField(
            model_name='audio',
            name='type',
            field=models.CharField(default=1, max_length=255, choices=[(b'1', b'Single'), (b'2', b'Album'), (b'3', b'Remix')]),
        ),
        migrations.AlterField(
            model_name='video',
            name='privacy',
            field=models.CharField(default=b'public', max_length=255, choices=[(b'private', b'Private'), (b'public', b'Public')]),
        ),
        migrations.AlterField(
            model_name='video',
            name='type',
            field=models.CharField(default=1, max_length=255, choices=[(b'1', b'Single'), (b'2', b'Album'), (b'3', b'Remix')]),
        ),
    ]
