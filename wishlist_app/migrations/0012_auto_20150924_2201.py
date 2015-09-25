# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0011_auto_20150924_2158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='claim_date',
        ),
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 24, 22, 1, 26, 871000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 24, 22, 1, 26, 871000)),
        ),
    ]
