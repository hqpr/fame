# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0035_audio_soundcloud_track_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('time_specific', models.BooleanField(default=False)),
                ('time', models.CharField(max_length=255)),
                ('approved', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('fan', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(to='media.Video')),
            ],
            options={
                'db_table': 'video_comments',
            },
        ),
        migrations.CreateModel(
            name='VideoLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('fan', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(to='media.Video')),
            ],
            options={
                'db_table': 'video_likes',
            },
        ),
        migrations.AlterUniqueTogether(
            name='videolike',
            unique_together=set([('video', 'fan')]),
        ),
    ]
