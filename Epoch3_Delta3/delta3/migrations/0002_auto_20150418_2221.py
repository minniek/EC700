# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delta3', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='search',
            old_name='url_gif',
            new_name='gif_url',
        ),
    ]
