# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 19, 38, 636000))),
                ('modified_date', models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 19, 38, 636000))),
                ('created_by', models.ForeignKey(related_name='groupmember_created_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 19, 38, 636000))),
                ('modified_date', models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 19, 38, 636000))),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default=None, null=True, blank=True)),
                ('link', models.TextField(default=None, null=True, blank=True)),
                ('quantity', models.IntegerField(default=1, null=True, blank=True)),
                ('claimed', models.BooleanField(default=False)),
                ('claim_date', models.DateField(default=None, null=True, blank=True)),
                ('purchased', models.BooleanField(default=False)),
                ('purchase_date', models.DateField(default=None, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='item_created_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('giver', models.ForeignKey(related_name='wishlist_giver', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 19, 38, 636000))),
                ('modified_date', models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 19, 38, 636000))),
                ('created_by', models.ForeignKey(related_name='role_created_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='role_modified_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WishlistGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 19, 38, 636000))),
                ('modified_date', models.DateTimeField(default=datetime.datetime(2015, 9, 17, 21, 19, 38, 636000))),
                ('name', models.CharField(default=None, max_length=200)),
                ('description', models.TextField(null=True, blank=True)),
                ('end_date', models.DateTimeField(default=None, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='wishlistgroup_created_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('creator', models.ForeignKey(related_name='group_creator', default=None, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='wishlistgroup_modified_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='item',
            name='group',
            field=models.ForeignKey(related_name='wishlist_group', to='wishlist_app.WishlistGroup'),
        ),
        migrations.AddField(
            model_name='item',
            name='modified_by',
            field=models.ForeignKey(related_name='item_modified_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='wisher',
            field=models.ForeignKey(related_name='wishlist_wisher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='group',
            field=models.ForeignKey(related_name='group_member_wishlistgroup', to='wishlist_app.WishlistGroup'),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='modified_by',
            field=models.ForeignKey(related_name='groupmember_modified_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='user',
            field=models.ForeignKey(related_name='group_member_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
