# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_type', models.CharField(max_length=100, choices=[(1, b'Artist'), (2, b'Music Explorer'), (3, b'Music Industry')])),
                ('display_name', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('picture', models.ImageField(upload_to=b'avatars')),
                ('artist_name', models.CharField(max_length=100, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
