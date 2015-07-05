# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BlogItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('publish_date', models.DateField(auto_now=True)),
                ('published', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('snippet', models.CharField(max_length=255)),
                ('thumbnail', models.ImageField(upload_to=b'blog/%y/%m/%d')),
                ('cover_image', models.ImageField(upload_to=b'blog/%y/%m/%d')),
                ('comments_open', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogItemCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blog_category', models.ForeignKey(to='blog.BlogCategory')),
                ('blog_item', models.ForeignKey(to='blog.BlogItem')),
            ],
        ),
        migrations.CreateModel(
            name='BlogItemComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('blog_item', models.ForeignKey(to='blog.BlogItem')),
                ('reply_to', models.ForeignKey(related_name='in_response_to', blank=True, to='blog.BlogItemComment', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogItemTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blog_item', models.ForeignKey(to='blog.BlogItem')),
            ],
        ),
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='blogitemtag',
            name='blog_tag',
            field=models.ForeignKey(to='blog.BlogTag'),
        ),
        migrations.AddField(
            model_name='blogauthor',
            name='blog_item',
            field=models.ForeignKey(to='blog.BlogItem'),
        ),
    ]
