# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0007_audio_is_complete'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoPlaylist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('videos', models.ManyToManyField(to='media.Video', null=True, blank=True)),
            ],
        ),
    ]
