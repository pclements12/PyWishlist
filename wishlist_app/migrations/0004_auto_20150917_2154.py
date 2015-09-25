# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wishlist_app', '0003_auto_20150917_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlistgroup',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 54, 53, 732000)),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 54, 53, 732000)),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 54, 53, 732000)),
        ),
        migrations.AlterField(
            model_name='item',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 54, 53, 732000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 54, 53, 732000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 54, 53, 732000)),
        ),
        migrations.AlterField(
            model_name='wishlistgroup',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 54, 53, 732000)),
        ),
        migrations.AlterField(
            model_name='wishlistgroup',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 54, 53, 732000)),
        ),
    ]
