# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-27 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='charge_id',
            field=models.CharField(default=1, max_length=234),
            preserve_default=False,
        ),
    ]