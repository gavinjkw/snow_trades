# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-25 22:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('size', models.CharField(max_length=50)),
                ('isUsed', models.BooleanField(default=True)),
                ('condition', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=70)),
                ('access_level', models.IntegerField(default=1)),
                ('hashed_pass', models.CharField(max_length=70)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_added', to='store.User'),
        ),
    ]
