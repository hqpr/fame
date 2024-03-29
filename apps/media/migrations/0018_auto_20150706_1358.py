# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0017_auto_20150702_1012'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('audio', models.ForeignKey(to='media.Audio')),
                ('fan', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'audio_likes',
            },
        ),
        migrations.AlterUniqueTogether(
            name='audiolike',
            unique_together=set([('audio', 'fan')]),
        ),
    ]
