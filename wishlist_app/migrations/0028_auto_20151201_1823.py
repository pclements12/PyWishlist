# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from wishlist_app.models import GroupItem, Item, ItemComment


def data_migration(apps, schema_editor):
    # collect items
    #   create group items for each
    # collect item comments
    #   match item comments to group_items (nulling item as we map to group_item)

    for item in Item.objects.all():
        print "Migrating item %s, in group %s" % (item, item.group)
        group_item = GroupItem(item=item, group=item.group)
        group_item.save()
        print "Group Item mapping created successfully"

    for item_comment in ItemComment.objects.all():
        print "Migrating item comment %s, %s" % (item_comment.item.group, item_comment.item)
        group_item = GroupItem.objects.get(group=item_comment.item.group, item=item_comment.item)
        item_comment.group_item = group_item
        # item_comment.item = None
        item_comment.save()


def backwards_migration(apps, schema_editor):
    print "beginning backwards migration"
    for group_item in GroupItem.objects.all():
        group_item.item.group = group_item.group


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0027_auto_20151201_1818'),
    ]

    operations = [
        migrations.RunPython(data_migration, backwards_migration),
    ]
