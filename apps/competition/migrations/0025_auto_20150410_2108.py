# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0024_auto_20150410_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competitionentryaudio',
            old_name='audio',
            new_name='entry',
        ),
        migrations.RenameField(
            model_name='competitionentryimage',
            old_name='image',
            new_name='entry',
        ),
        migrations.RenameField(
            model_name='competitionentryvideo',
            old_name='video',
            new_name='entry',
        ),
        migrations.AlterUniqueTogether(
            name='competitionentryaudio',
            unique_together=set([('competition_entry', 'entry')]),
        ),
        migrations.AlterUniqueTogether(
            name='competitionentryimage',
            unique_together=set([('competition_entry', 'entry')]),
        ),
        migrations.AlterUniqueTogether(
            name='competitionentryvideo',
            unique_together=set([('competition_entry', 'entry')]),
        ),
    ]
