# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-28 23:15
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0082_auto_20180429_0212'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Audience',
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='created_at',
            field=models.IntegerField(default=1524957333, editable=False),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='rfid',
            field=models.CharField(default=uuid.UUID('0d2830b4-4b3a-11e8-8fba-00005ae50095'), editable=False, max_length=256),
        ),
    ]
