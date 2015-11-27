# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0025_comment_hide_from_wisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secretsantaassignment',
            name='giver',
            field=models.ForeignKey(related_name='santa_giver', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
