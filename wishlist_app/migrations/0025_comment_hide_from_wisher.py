# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist_app', '0024_auto_20151109_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='hide_from_wisher',
            field=models.BooleanField(default=False),
        ),
    ]
