# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0023_auto_20151021_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invite',
            old_name='on',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='invite',
            old_name='by',
            new_name='inviter',
        ),
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 21, 15, 31, 47, 627000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 21, 15, 31, 47, 627000)),
        ),
    ]
