# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tips',
            name='step1',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tips',
            name='step2',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tips',
            name='step3',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tips',
            name='step4',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tips',
            name='step5',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tips',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
