# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 14:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lowfat', '0087_historicalblog_historicalclaimant_historicalexpense_historicalfund_historicalgeneralsentmail'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalsentmail',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='historicalgeneralsentmail',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
