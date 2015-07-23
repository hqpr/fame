# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0026_userstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfluencer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('influencer', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='userprofile.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UserTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='userprofile.UserProfile')),
            ],
        ),
    ]
