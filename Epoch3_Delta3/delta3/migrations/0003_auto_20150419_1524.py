# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delta3', '0002_auto_20150418_2221'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Search',
            new_name='Gif',
        ),
        migrations.RenameModel(
            old_name='LoginInfo',
            new_name='User',
        ),
    ]
