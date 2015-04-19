# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_app', '0002_auto_20150419_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='field_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
