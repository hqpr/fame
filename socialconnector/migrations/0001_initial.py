# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAudio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255, choices=[(b'1', b'track_type_1'), (b'2', b'track_type_2'), (b'3', b'track_type_3'), (b'4', b'track_type_4')])),
                ('genre', models.CharField(default=b'rock', max_length=255, choices=[(b'rock', b'rock'), (b'pop', b'pop'), (b'classic', b'classic')])),
                ('description', models.TextField(null=True, blank=True)),
                ('bpm', models.CharField(max_length=255, null=True, blank=True)),
                ('privacy', models.CharField(default=b'public', max_length=255, choices=[(b'private', b'private'), (b'public', b'public')])),
                ('audio', models.FileField(upload_to=b'audios')),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('cover', models.FileField(null=True, upload_to=b'audios/covers', blank=True)),
                ('user', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.FileField(upload_to=b'photos')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video', models.FileField(upload_to=b'videos')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('cover', models.FileField(null=True, upload_to=b'videos/covers', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VideoPlaylist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('videos', models.ManyToManyField(to='socialconnector.UserVideo', null=True, blank=True)),
            ],
        ),
    ]
