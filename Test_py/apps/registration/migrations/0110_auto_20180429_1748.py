# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-29 14:48
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0109_auto_20180429_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='created_at',
            field=models.IntegerField(default=1525013327, editable=False),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='rfid',
            field=models.CharField(default=uuid.UUID('6c081d22-4bbc-11e8-b9b7-00005ae5db4f'), editable=False, max_length=256),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='isPassed',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
