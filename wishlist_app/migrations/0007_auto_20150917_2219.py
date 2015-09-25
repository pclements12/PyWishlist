# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0006_auto_20150917_2206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlistgroup',
            name='users',
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 22, 19, 50, 765000)),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 22, 19, 50, 765000)),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 22, 19, 50, 765000)),
        ),
        migrations.AlterField(
            model_name='item',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 22, 19, 50, 765000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 22, 19, 50, 765000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 22, 19, 50, 765000)),
        ),
        migrations.AlterField(
            model_name='wishlistgroup',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 22, 19, 50, 765000)),
        ),
        migrations.AlterField(
            model_name='wishlistgroup',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 22, 19, 50, 765000)),
        ),
    ]
