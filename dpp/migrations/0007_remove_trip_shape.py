# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-15 20:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dpp', '0006_auto_20170515_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='shape',
        ),
    ]