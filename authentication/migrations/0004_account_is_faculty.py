# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-25 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20171025_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_faculty',
            field=models.BooleanField(default=False),
        ),
    ]
