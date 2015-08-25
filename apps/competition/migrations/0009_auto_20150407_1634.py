# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0008_competitiontermsummary'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionTerms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('terms', models.TextField()),
                ('competition', models.OneToOneField(to='competition.Competition')),
            ],
            options={
                'db_table': 'competition_terms',
                'verbose_name_plural': 'Competition terms',
            },
        ),
        migrations.AlterModelOptions(
            name='competitiontermsummary',
            options={'verbose_name_plural': 'Competition terms - summaries'},
        ),
    ]
