# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import wishlist_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0015_auto_20150925_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=wishlist_app.models.generate_uuid, max_length=64, verbose_name='Activation key')),
                ('email', models.EmailField(max_length=254)),
                ('group', models.ForeignKey(related_name='invite_group', to='wishlist_app.WishlistGroup')),
            ],
        ),
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 10, 31, 9, 665000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 10, 31, 9, 665000)),
        ),
    ]
