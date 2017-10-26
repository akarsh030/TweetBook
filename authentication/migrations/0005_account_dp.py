# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-26 04:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_account_is_faculty'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='dp',
            field=models.FileField(default=django.utils.timezone.now, upload_to='dps/'),
            preserve_default=False,
        ),
    ]