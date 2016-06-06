# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-06 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fellowms', '0022_fellow_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ad_status',
            field=models.CharField(choices=[('U', 'Unprocessed'), ('V', 'Visible'), ('H', 'Hide'), ('A', 'Archived')], default='U', max_length=1),
        ),
    ]
