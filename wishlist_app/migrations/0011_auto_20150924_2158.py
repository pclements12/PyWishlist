# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0010_auto_20150924_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='claimed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 24, 21, 58, 19, 752000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 24, 21, 58, 19, 752000)),
        ),
    ]
