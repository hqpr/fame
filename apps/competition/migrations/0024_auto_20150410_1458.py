# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0023_auto_20150407_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionentrycomment',
            name='parent',
            field=models.ForeignKey(blank=True, to='competition.CompetitionEntryComment', null=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='slug',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='competitioncountry',
            unique_together=set([('competition', 'country')]),
        ),
        migrations.AlterUniqueTogether(
            name='competitionentry',
            unique_together=set([('competition', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='competitionentryaudio',
            unique_together=set([('competition_entry', 'audio')]),
        ),
        migrations.AlterUniqueTogether(
            name='competitiongenre',
            unique_together=set([('competition', 'genre')]),
        ),
        migrations.AlterUniqueTogether(
            name='competitionpartner',
            unique_together=set([('competition', 'partner')]),
        ),
        migrations.AlterUniqueTogether(
            name='competitionstagerequirement',
            unique_together=set([('competition_stage', 'media_type')]),
        ),
    ]
