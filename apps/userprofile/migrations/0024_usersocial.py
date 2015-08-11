# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0023_auto_20150715_0827'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=255, choices=[(b'instagram', b'Instagram'), (b'twitter', b'twitter'), (b'facebook', b'facebook'), (b'youtube', b'youtube'), (b'soundcloud', b'soundcloud'), (b'wavo', b'wavo'), (b'spotify', b'spotify'), (b'vimeo', b'vimeo')])),
                ('link', models.CharField(max_length=255)),
                ('user', models.ForeignKey(to='userprofile.UserProfile')),
            ],
        ),
    ]
