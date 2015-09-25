# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0009_auto_20150922_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmember',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='groupmember',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='groupmember',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='groupmember',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='item',
            name='claimed',
        ),
        migrations.RemoveField(
            model_name='item',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='item',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='item',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='item',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='item',
            name='purchase_date',
        ),
        migrations.RemoveField(
            model_name='item',
            name='purchased',
        ),
        migrations.RemoveField(
            model_name='wishlistgroup',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='wishlistgroup',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='wishlistgroup',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='wishlistgroup',
            name='modified_date',
        ),
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 24, 13, 28, 48, 160000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 24, 13, 28, 48, 160000)),
        ),
    ]
