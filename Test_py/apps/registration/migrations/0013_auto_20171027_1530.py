# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 12:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_auto_20171027_1529'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='qSubscriber',
            new_name='Subscriber',
        ),
    ]