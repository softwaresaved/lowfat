# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-12 10:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tagulous.models.fields
import tagulous.models.models

def copy_grant_info(apps, schema_editor):  # pylint: disable=unused-argument,invalid-name
    Fund = apps.get_model("lowfat", "Fund")  # pylint: disable=invalid-name
    for fund in Fund.objects.all():
        if fund.funds_from_default == "C":
            fund.grant = "{}/Continuing".format(fund.grant_default)
        elif fund.funds_from_default == "I":
            fund.grant = "{}/Core".format(fund.grant_default)
        elif fund.funds_from_default == "F":
            fund.grant = "{}/Fellowship".format(fund.grant_default)
        else:
            print("Fail {}.".format(fund))
        fund.save()

    Expense = apps.get_model("lowfat", "Expense")  # pylint: disable=invalid-name
    for expense in Expense.objects.all():
        if expense.funds_from == "C":
            expense.grant = "{}/Continuing".format(expense.grant_used)
        elif expense.funds_from == "I":
            expense.grant = "{}/Core".format(expense.grant_used)
        elif expense.funds_from == "F":
            expense.grant = "{}/Fellowship".format(expense.grant_used)
        else:
            print("Fail {}.".format(expense))
        expense.save()

class Migration(migrations.Migration):

    dependencies = [
        ('lowfat', '0127_auto_20180412_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
                ('path', models.TextField()),
                ('label', models.CharField(help_text='The name of the tag, without ancestors', max_length=255)),
                ('level', models.IntegerField(default=1, help_text='The level of the tag in the tree')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='lowfat.Grant')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
            bases=(tagulous.models.models.BaseTagTreeModel, models.Model),
        ),
        migrations.AddField(
            model_name='expense',
            name='grant',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, autocomplete_view=None, default='SSI2/Fellowship', force_lowercase=True, help_text='Enter a comma-separated tag string', initial='SSI1, SSI1/Core, SSI1/Fellowship, SSI1/Continuing, SSI2, SSI2/Core, SSI2/Fellowship, SSI2/Continuing, SSI3, SSI3/Core, SSI3/Fellowship, SSI3/Continuing', to='lowfat.Grant', tree=True),
        ),
        migrations.AddField(
            model_name='fund',
            name='grant',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, autocomplete_view=None, default='SSI2/Fellowship', force_lowercase=True, help_text='Enter a comma-separated tag string', initial='SSI1, SSI1/Core, SSI1/Fellowship, SSI1/Continuing, SSI2, SSI2/Core, SSI2/Fellowship, SSI2/Continuing, SSI3, SSI3/Core, SSI3/Fellowship, SSI3/Continuing', to='lowfat.Grant', tree=True),
        ),
        migrations.AlterUniqueTogether(
            name='grant',
            unique_together=set([('slug', 'parent')]),
        ),
        migrations.RunPython(
            copy_grant_info
        ),
    ]
