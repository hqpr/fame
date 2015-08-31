# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0034_auto_20150825_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionFeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_type', models.CharField(max_length=255, choices=[(b'uploaded_track', b'User uploaded a track'), (b'uploaded_video', b'User uploaded a video'), (b'playlist_created', b'User created a playlist'), (b'entered_competition', b'User entered a competition')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
