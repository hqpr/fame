# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competition', '0020_competitionentry_knocked_out'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionEntryComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('competition_entry', models.ForeignKey(to='competition.CompetitionEntry')),
                ('fan', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'competition_entry_comments',
            },
        ),
        migrations.CreateModel(
            name='CompetitionEntryLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('competition_entry', models.ForeignKey(to='competition.CompetitionEntry')),
                ('fan', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'competition_entry_likes',
            },
        ),
        migrations.CreateModel(
            name='CompetitionEntryRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('competition_entry', models.ForeignKey(to='competition.CompetitionEntry')),
            ],
            options={
                'db_table': 'competition_entry_rating',
            },
        ),
        migrations.CreateModel(
            name='CompetitionJudge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competition', models.ForeignKey(to='competition.Competition')),
                ('judge', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'competition_judges',
            },
        ),
        migrations.AddField(
            model_name='competitionentryrating',
            name='judge',
            field=models.ForeignKey(to='competition.CompetitionJudge'),
        ),
        migrations.AlterUniqueTogether(
            name='competitionentryrating',
            unique_together=set([('competition_entry', 'judge')]),
        ),
        migrations.AlterUniqueTogether(
            name='competitionentrylike',
            unique_together=set([('competition_entry', 'fan')]),
        ),
    ]
