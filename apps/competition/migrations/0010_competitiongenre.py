# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
        ('competition', '0009_auto_20150407_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionGenre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competition', models.ForeignKey(to='competition.Competition')),
                ('genre', models.ForeignKey(to='media.Genre')),
            ],
            options={
                'db_table': 'competition_genres',
            },
        ),
    ]
