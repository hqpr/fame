# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0028_competitionvisual_entry_instructions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionChart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_score', models.PositiveIntegerField()),
                ('plays', models.PositiveIntegerField()),
                ('entry', models.ForeignKey(to='competition.CompetitionEntry')),
            ],
        ),
        migrations.AddField(
            model_name='competition',
            name='valid',
            field=models.BooleanField(default=False),
        ),
    ]
