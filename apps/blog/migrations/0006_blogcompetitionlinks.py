# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0034_competition_competition_tagline'),
        ('blog', '0005_auto_20150706_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCompetitionLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blog_item', models.ForeignKey(to='blog.BlogItem')),
                ('competition', models.ForeignKey(to='competition.Competition')),
            ],
        ),
    ]
