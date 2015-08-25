# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0020_auto_20150706_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioPlaylist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('artist', models.CharField(default=None, max_length=255)),
                ('privacy', models.CharField(default=None, max_length=100)),
                ('description', models.TextField(default=None)),
                ('cover', models.ImageField(null=True, upload_to=b'playlists/%y/%m/%d', blank=True)),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('genre', models.ForeignKey(default=1, to='media.Genre')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField()),
                ('audio', models.ForeignKey(to='media.Audio')),
                ('playlist', models.ForeignKey(to='media.AudioPlaylist')),
            ],
            options={
                'db_table': 'playlist_item',
            },
        ),
        migrations.AlterUniqueTogether(
            name='playlistitem',
            unique_together=set([('playlist', 'audio')]),
        ),
    ]
