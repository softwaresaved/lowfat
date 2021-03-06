# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lowfat', '0006_auto_20160414_1132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fellow',
            old_name='full_name',
            new_name='surname',
        ),
        migrations.AddField(
            model_name='fellow',
            name='affiliation',
            field=models.CharField(default='', max_length=120, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fellow',
            name='forenames',
            field=models.CharField(default='', max_length=120, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fellow',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('R', 'Rather not say')], default='R', max_length=1),
        ),
        migrations.AddField(
            model_name='fellow',
            name='phone',
            field=models.CharField(default='', max_length=14, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fellow',
            name='research_area',
            field=models.CharField(default='', max_length=4, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fellow',
            name='work_description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fellow',
            name='year',
            field=models.IntegerField(default=2017),
        ),
    ]
