# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wishlist_app', '0013_auto_20150924_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlistgroup',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='wishlist_app.GroupMember'),
        ),
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 10, 1, 21, 672000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 10, 1, 21, 672000)),
        ),
    ]
