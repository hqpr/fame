# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0015_auto_20150702_0959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='added',
        ),
        migrations.RemoveField(
            model_name='video',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='video',
            name='bpm',
        ),
        migrations.RemoveField(
            model_name='video',
            name='cover',
        ),
        migrations.RemoveField(
            model_name='video',
            name='description',
        ),
        migrations.RemoveField(
            model_name='video',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='video',
            name='id',
        ),
        migrations.RemoveField(
            model_name='video',
            name='is_complete',
        ),
        migrations.RemoveField(
            model_name='video',
            name='name',
        ),
        migrations.RemoveField(
            model_name='video',
            name='privacy',
        ),
        migrations.RemoveField(
            model_name='video',
            name='type',
        ),
        migrations.RemoveField(
            model_name='video',
            name='uid',
        ),
        migrations.RemoveField(
            model_name='video',
            name='user',
        ),
        migrations.AddField(
            model_name='video',
            name='audio_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default='', serialize=False, to='media.Audio'),
            preserve_default=False,
        ),
    ]
