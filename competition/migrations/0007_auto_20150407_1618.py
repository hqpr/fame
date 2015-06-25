# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0006_competitioncountry'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionPrize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prize', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=b'prizes/%y/%m/%d')),
                ('ordering', models.PositiveIntegerField()),
                ('competition', models.ForeignKey(to='competition.Competition')),
            ],
            options={
                'db_table': 'competition_prizes',
            },
        ),
        migrations.AlterModelOptions(
            name='competitioncountry',
            options={'verbose_name_plural': 'Competition countries'},
        ),
    ]
