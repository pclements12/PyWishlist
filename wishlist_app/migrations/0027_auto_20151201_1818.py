# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0026_auto_20151127_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comments', models.ManyToManyField(to='wishlist_app.Comment', through='wishlist_app.ItemComment')),
                ('group', models.ForeignKey(related_name='group_item_wishlistgroup', to='wishlist_app.WishlistGroup')),
                ('item', models.ForeignKey(related_name='group_item_item', to='wishlist_app.Item')),
            ],
        ),
        migrations.AddField(
            model_name='itemcomment',
            name='group_item',
            field=models.ForeignKey(related_name='itemcomment_group_item', to='wishlist_app.GroupItem', null=True),
        ),
    ]
