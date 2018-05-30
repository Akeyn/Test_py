# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-29 13:14
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0095_auto_20180429_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='created_at',
            field=models.IntegerField(default=1525007663, editable=False),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='rfid',
            field=models.CharField(default=uuid.UUID('3c64100a-4baf-11e8-9e72-00005ae5c52f'), editable=False, max_length=256),
        ),
    ]
