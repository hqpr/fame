# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255, choices=[(b'1', b'Single'), (b'2', b'Ketchup'), (b'3', b'Relish')])),
                ('genre', models.CharField(default=b'pop', max_length=255, choices=[(b'rock', b'Rock'), (b'pop', b'Pop'), (b'classic', b'Classic'), (b'electro', b'Electro')])),
                ('description', models.TextField(null=True, blank=True)),
                ('bpm', models.CharField(max_length=255, null=True, blank=True)),
                ('privacy', models.CharField(default=b'public', max_length=255, choices=[(b'private', b'private'), (b'public', b'public')])),
                ('audio', models.FileField(upload_to=b'audios')),
                ('added', models.DateTimeField(auto_now_add=True, null=True)),
                ('cover', models.FileField(null=True, upload_to=b'audios/covers', blank=True)),
                ('user', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
