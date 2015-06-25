# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0004_auto_20150407_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionVisual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('landing_page_content', models.TextField(null=True, blank=True)),
                ('landing_page_image', models.ImageField(null=True, upload_to=b'%y/%m/%d', blank=True)),
                ('landing_page_video_url', models.CharField(max_length=255, null=True, blank=True)),
                ('competition', models.OneToOneField(to='competition.Competition')),
            ],
            options={
                'db_table': 'competition_visuals',
            },
        ),
    ]
