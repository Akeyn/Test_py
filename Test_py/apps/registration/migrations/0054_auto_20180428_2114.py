# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-28 18:14
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0053_auto_20180428_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='created_at',
            field=models.IntegerField(default=1524939280),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='rfid',
            field=models.CharField(default=uuid.UUID('04bbac22-4b10-11e8-b0be-00005ae4ba10'), max_length=256),
        ),
    ]
