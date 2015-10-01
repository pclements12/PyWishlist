# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wishlist_app', '0016_auto_20150925_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistryAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='SecretSantaAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('giver', models.ForeignKey(related_name='santa_giver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='wishlistgroup',
            name='type',
            field=models.CharField(default=b'regular', max_length=30, choices=[(b'regular', b'Individual Wishlists'), (b'secret_santa', b'Secret Santa'), (b'registry', b'Registry/Birthday')]),
        ),
        migrations.AlterField(
            model_name='role',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 1, 13, 18, 56, 266000)),
        ),
        migrations.AlterField(
            model_name='role',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 1, 13, 18, 56, 266000)),
        ),
        migrations.AddField(
            model_name='secretsantaassignment',
            name='group',
            field=models.ForeignKey(related_name='santa_group', to='wishlist_app.WishlistGroup'),
        ),
        migrations.AddField(
            model_name='secretsantaassignment',
            name='wisher',
            field=models.ForeignKey(related_name='santa_wisher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='registryassignment',
            name='group',
            field=models.ForeignKey(related_name='registry_group', to='wishlist_app.WishlistGroup'),
        ),
        migrations.AddField(
            model_name='registryassignment',
            name='wisher',
            field=models.ForeignKey(related_name='registry_wisher', to=settings.AUTH_USER_MODEL),
        ),
    ]
