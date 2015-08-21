# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='user',
            new_name='sender',
        ),
        migrations.AddField(
            model_name='message',
            name='text',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
