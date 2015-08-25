# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0007_auto_20150407_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionTermSummary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.TextField()),
                ('ordering', models.PositiveIntegerField()),
                ('competition', models.ForeignKey(to='competition.Competition')),
            ],
            options={
                'db_table': 'competition_term_summaries',
            },
        ),
    ]
