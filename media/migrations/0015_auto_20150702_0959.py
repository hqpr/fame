# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0014_auto_20150626_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='artist',
            field=models.CharField(default=None, max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='bpm',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='cover',
            field=models.FileField(null=True, upload_to=b'videos/covers/%y/%m/%d', blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='genre',
            field=models.ForeignKey(blank=True, to='media.Genre', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='privacy',
            field=models.CharField(default=b'public', max_length=255, choices=[(b'private', b'private'), (b'public', b'public')]),
        ),
        migrations.AddField(
            model_name='video',
            name='type',
            field=models.CharField(default=1, max_length=255, choices=[(b'1', b'Single'), (b'2', b'Ketchup'), (b'3', b'Relish')]),
        ),
        migrations.AddField(
            model_name='video',
            name='video',
            field=models.FileField(default='default.mp4', upload_to=b'videos/%y/%m/%d'),
            preserve_default=False,
        ),
    ]
