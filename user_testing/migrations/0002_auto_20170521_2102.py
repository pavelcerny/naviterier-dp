# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-21 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_testing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='fromMyTesting',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='experiment',
            name='realGpsLat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='experiment',
            name='realGpsLon',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='experiment',
            name='successFail',
            field=models.BooleanField(default=False),
        ),
    ]
