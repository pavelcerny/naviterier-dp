# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-10 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naviterier', '0003_auto_20170510_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='street_noaccents',
            field=models.CharField(default='simple text', max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=40),
        ),
    ]
