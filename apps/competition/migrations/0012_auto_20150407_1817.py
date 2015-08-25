# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0011_auto_20150407_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionStage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('voting_public', models.BooleanField(default=True, verbose_name=b'Public voting allowed')),
                ('voting_judges', models.BooleanField(default=False, verbose_name=b'Judges voting allowed')),
                ('knockout_stage', models.BooleanField(default=False)),
                ('knockout_stage_limit', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'competition_stages',
            },
        ),
        migrations.AddField(
            model_name='competition',
            name='judge_weighting',
            field=models.PositiveIntegerField(default=500),
        ),
        migrations.AddField(
            model_name='competitionstage',
            name='competition',
            field=models.ForeignKey(to='competition.Competition'),
        ),
    ]
