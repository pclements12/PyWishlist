# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0017_auto_20151001_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 1, 14, 28, 31, 58000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 1, 14, 28, 31, 58000)),
        ),
        migrations.AlterUniqueTogether(
            name='registryassignment',
            unique_together=set([('group', 'wisher')]),
        ),
        migrations.AlterUniqueTogether(
            name='secretsantaassignment',
            unique_together=set([('group', 'wisher', 'giver')]),
        ),
    ]
