# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-16 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0045_auto_20171216_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='created_at',
            field=models.IntegerField(default=1513417725),
        ),
    ]
