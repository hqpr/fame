# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_audio_image_video'),
        ('competition', '0018_auto_20150407_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionEntryAudio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('audio', models.ForeignKey(to='media.Audio')),
                ('competition_entry', models.ForeignKey(to='competition.CompetitionEntry')),
                ('competition_stage_requirement', models.ForeignKey(to='competition.CompetitionStageRequirement')),
            ],
            options={
                'db_table': 'competition_entry_audio',
                'verbose_name_plural': 'Competition Entry Audio',
            },
        ),
        migrations.CreateModel(
            name='CompetitionEntryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competition_entry', models.ForeignKey(to='competition.CompetitionEntry')),
                ('competition_stage_requirement', models.ForeignKey(to='competition.CompetitionStageRequirement')),
                ('image', models.ForeignKey(to='media.Image')),
            ],
            options={
                'db_table': 'competition_entry_image',
                'verbose_name_plural': 'Competition Entry Image',
            },
        ),
        migrations.CreateModel(
            name='CompetitionEntryVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competition_entry', models.ForeignKey(to='competition.CompetitionEntry')),
                ('competition_stage_requirement', models.ForeignKey(to='competition.CompetitionStageRequirement')),
                ('video', models.ForeignKey(to='media.Video')),
            ],
            options={
                'db_table': 'competition_entry_video',
                'verbose_name_plural': 'Competition Entry Video',
            },
        ),
    ]
