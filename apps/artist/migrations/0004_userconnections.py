# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artist', '0003_auto_20150622_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserConnections',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('connection', models.ForeignKey(related_name='connection', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='follower', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_connections',
            },
        ),
    ]
