# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-09 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0031_auto_20171116_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber_Meter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber_id', models.BigIntegerField()),
                ('meter_id', models.BigIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='created_at',
            field=models.IntegerField(default=1512837763),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Picture'),
        ),
    ]