# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-14 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lowfat', '0118_auto_20171214_0715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='status',
            field=models.CharField(choices=[('U', 'Waiting for triage'), ('R', 'Waiting to be reviewed'), ('C', 'Reviewing loop'), ('G', 'Waiting to be proofread'), ('L', 'Waiting to be published'), ('P', 'Published'), ('M', 'Mistaked'), ('D', 'Rejected'), ('O', 'Out of date'), ('X', 'Remove')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='historicalblog',
            name='status',
            field=models.CharField(choices=[('U', 'Waiting for triage'), ('R', 'Waiting to be reviewed'), ('C', 'Reviewing loop'), ('G', 'Waiting to be proofread'), ('L', 'Waiting to be published'), ('P', 'Published'), ('M', 'Mistaked'), ('D', 'Rejected'), ('O', 'Out of date'), ('X', 'Remove')], default='U', max_length=1),
        ),
    ]
