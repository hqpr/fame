# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0005_auto_20150609_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='audio',
            field=models.FileField(default=b'default.mp3', upload_to=b'audios'),
        ),
        migrations.AddField(
            model_name='audio',
            name='bpm',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='cover',
            field=models.FileField(null=True, upload_to=b'audios/covers', blank=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='genre',
            field=models.CharField(default=b'pop', max_length=255, choices=[(b'rock', b'Rock'), (b'pop', b'Pop'), (b'classic', b'Classic'), (b'electro', b'Electro')]),
        ),
        migrations.AddField(
            model_name='audio',
            name='privacy',
            field=models.CharField(default=b'public', max_length=255, choices=[(b'private', b'private'), (b'public', b'public')]),
        ),
        migrations.AddField(
            model_name='audio',
            name='type',
            field=models.CharField(default=1, max_length=255, choices=[(b'1', b'Single'), (b'2', b'Ketchup'), (b'3', b'Relish')]),
        ),
    ]
