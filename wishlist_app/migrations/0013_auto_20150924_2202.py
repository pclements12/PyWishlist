# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0012_auto_20150924_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 24, 22, 2, 9, 927000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 24, 22, 2, 9, 928000)),
        ),
        migrations.AlterField(
            model_name='wishlistgroup',
            name='end_date',
            field=models.DateField(default=None, null=True, blank=True),
        ),
    ]
