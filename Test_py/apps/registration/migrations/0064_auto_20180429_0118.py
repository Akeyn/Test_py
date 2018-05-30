# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-28 22:18
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0063_auto_20180429_0117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture', models.IntegerField()),
                ('audience_name', models.IntegerField(blank=True, null=True)),
                ('day', models.DateField(blank=True, null=True)),
                ('lecturer', models.CharField(blank=True, choices=[('b8115390-4af6-11e8-996a-00005ae48f9e', 'Qwe'), ('e8b56168-4b0f-11e8-ac7f-00005ae4b9e1', 'qaz')], max_length=256, null=True)),
                ('isPassed', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='created_at',
            field=models.IntegerField(default=1524953889),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='rfid',
            field=models.CharField(default=uuid.UUID('08185c38-4b32-11e8-8ff3-00005ae4f321'), max_length=256),
        ),
    ]
