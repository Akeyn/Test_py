# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countries',
            name='country_code',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='countries',
            name='country_name',
            field=models.TextField(max_length=32, validators=['^[A-Z]']),
        ),
    ]
