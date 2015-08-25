# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0005_competitionvisual'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionCountry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('competition', models.ForeignKey(to='competition.Competition')),
            ],
            options={
                'db_table': 'competition_countries',
            },
        ),
    ]
