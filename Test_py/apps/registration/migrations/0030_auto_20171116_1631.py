# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0029_auto_20171116_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='created_at',
            field=models.IntegerField(default=1510842702),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='images/', verbose_name='Изображение'),
        ),
    ]
