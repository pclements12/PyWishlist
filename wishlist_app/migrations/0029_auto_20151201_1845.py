# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0028_auto_20151201_1823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='item',
            name='group',
        ),
        migrations.RemoveField(
            model_name='itemcomment',
            name='item',
        ),
        migrations.AlterField(
            model_name='itemcomment',
            name='group_item',
            field=models.ForeignKey(related_name='itemcomment_group_item', to='wishlist_app.GroupItem'),
        ),
    ]
