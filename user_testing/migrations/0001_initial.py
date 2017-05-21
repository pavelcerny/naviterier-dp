# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-21 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('estimatedGpsLat', models.FloatField(default=0)),
                ('estimatedGpsLon', models.FloatField(default=0)),
                ('estimatedAddressLat', models.FloatField(default=0)),
                ('estimatedAddressLon', models.FloatField(default=0)),
                ('estimatedAddress', models.CharField(max_length=150)),
                ('recordTime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RecordedAfterCorner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(default=0)),
                ('lon', models.FloatField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RecordedBeforeCorner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(default=0)),
                ('lon', models.FloatField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
