# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('country_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('country_code', models.TextField()),
                ('country_name', models.TextField()),
            ],
        ),
    ]