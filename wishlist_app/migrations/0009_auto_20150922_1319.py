# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0008_auto_20150917_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmember',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 13, 19, 45, 853000)),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 13, 19, 45, 853000)),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 13, 19, 45, 853000)),
        ),
        migrations.AlterField(
            model_name='item',
            name='link',
            field=models.URLField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 13, 19, 45, 853000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 13, 19, 45, 853000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 13, 19, 45, 853000)),
        ),
        migrations.AlterField(
            model_name='wishlistgroup',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 13, 19, 45, 853000)),
        ),
        migrations.AlterField(
            model_name='wishlistgroup',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 13, 19, 45, 853000)),
        ),
    ]
