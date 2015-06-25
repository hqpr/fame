# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0014_competitionstage_final_stage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionStageRequirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('media_type', models.CharField(max_length=10, choices=[(b'audio', b'Audio'), (b'image', b'Image'), (b'video', b'Video')])),
                ('total_required', models.PositiveIntegerField()),
                ('ordering', models.PositiveIntegerField()),
                ('competition_stage', models.ForeignKey(to='competition.CompetitionStage')),
            ],
            options={
                'db_table': 'competition_stage_requirements',
            },
        ),
    ]
