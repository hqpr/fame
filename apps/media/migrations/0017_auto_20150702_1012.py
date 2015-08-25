# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0016_auto_20150702_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='audio_ptr',
        ),
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
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='name',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
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
            name='uid',
            field=models.CharField(max_length=11, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
