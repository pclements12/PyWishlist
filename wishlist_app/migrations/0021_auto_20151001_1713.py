# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0020_auto_20151001_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 1, 17, 13, 1, 159000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 1, 17, 13, 1, 159000)),
        ),
        migrations.AlterField(
            model_name='secretsantaassignment',
            name='giver',
            field=models.ForeignKey(related_name='santa_giver', default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
