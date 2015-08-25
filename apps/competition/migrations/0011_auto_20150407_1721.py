# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0010_competitiongenre'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionPartner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.PositiveIntegerField()),
                ('competition', models.ForeignKey(to='competition.Competition')),
            ],
            options={
                'db_table': 'competition_partners',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('logo', models.ImageField(upload_to=b'partners/%y/%m/%d')),
                ('link', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'partners',
            },
        ),
        migrations.AddField(
            model_name='competitionpartner',
            name='partner',
            field=models.ForeignKey(to='competition.Partner'),
        ),
    ]
