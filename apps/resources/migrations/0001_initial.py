# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competition', '0035_competitionentryrating_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourcesAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResourcesCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('slug', models.CharField(max_length=255, unique=True, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ResourcesCompetitionLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResourcesItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('publish_date', models.DateTimeField()),
                ('published', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('snippet', models.CharField(max_length=255)),
                ('thumbnail', models.ImageField(upload_to=b'resources/%y/%m/%d')),
                ('cover_image', models.ImageField(upload_to=b'resources/%y/%m/%d')),
                ('comments_open', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ResourcesItemCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resource_category', models.ForeignKey(to='resources.ResourcesCategory')),
                ('resource_item', models.ForeignKey(to='resources.ResourcesItem')),
            ],
        ),
        migrations.CreateModel(
            name='ResourcesItemComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('reply_to', models.ForeignKey(related_name='in_response_to', blank=True, to='resources.ResourcesItemComment', null=True)),
                ('resource_item', models.ForeignKey(to='resources.ResourcesItem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResourcesItemTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resource_item', models.ForeignKey(to='resources.ResourcesItem')),
            ],
        ),
        migrations.CreateModel(
            name='ResourcesTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('slug', models.CharField(max_length=255, unique=True, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='resourcesitemtag',
            name='resource_tag',
            field=models.ForeignKey(to='resources.ResourcesTag'),
        ),
        migrations.AddField(
            model_name='resourcescompetitionlinks',
            name='blog_item',
            field=models.ForeignKey(to='resources.ResourcesItem'),
        ),
        migrations.AddField(
            model_name='resourcescompetitionlinks',
            name='competition',
            field=models.ForeignKey(to='competition.Competition'),
        ),
        migrations.AddField(
            model_name='resourcesauthor',
            name='resource_item',
            field=models.ForeignKey(to='resources.ResourcesItem'),
        ),
    ]
