# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20171026_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='country',
            field=models.CharField(max_length=32),
        ),
    ]
