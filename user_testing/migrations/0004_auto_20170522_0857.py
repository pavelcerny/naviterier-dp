# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 06:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_testing', '0003_auto_20170521_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordedaftercorner',
            name='experiment',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user_testing.Experiment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recordedbeforecorner',
            name='experiment',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='user_testing.Experiment'),
            preserve_default=False,
        ),
    ]
