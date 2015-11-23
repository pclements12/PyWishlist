# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wishlist_app', '0023_auto_20151021_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Created Date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name=b'Modified Date')),
                ('anonymous', models.BooleanField(default=False)),
                ('text', models.TextField()),
                ('commenter', models.ForeignKey(related_name='comment_commenter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.ForeignKey(related_name='groupcomment_comment', to='wishlist_app.WishlistGroup')),
                ('group', models.ForeignKey(related_name='groupcomment_group', to='wishlist_app.WishlistGroup')),
            ],
        ),
        migrations.CreateModel(
            name='ItemComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.ForeignKey(related_name='itemcomment_comment', to='wishlist_app.Comment')),
                ('item', models.ForeignKey(related_name='itemcomment_item', to='wishlist_app.Item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='comments',
            field=models.ManyToManyField(to='wishlist_app.Comment', through='wishlist_app.ItemComment'),
        ),
    ]
