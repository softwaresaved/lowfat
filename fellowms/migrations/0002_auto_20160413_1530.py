# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-13 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fellowms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fellow',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fellow',
            name='email',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]
