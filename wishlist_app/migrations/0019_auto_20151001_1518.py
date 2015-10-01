# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0018_auto_20151001_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registryassignment',
            name='group',
            field=models.OneToOneField(related_name='registry_group', to='wishlist_app.WishlistGroup'),
        ),
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 1, 15, 18, 16, 791000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 1, 15, 18, 16, 791000)),
        ),
    ]
