# Generated by Django 4.2 on 2024-12-10 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lowfat', '0161_claimant_supplier_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fund',
            name='direct_invoice',
        ),
        migrations.RemoveField(
            model_name='historicalfund',
            name='direct_invoice',
        ),
        migrations.AddField(
            model_name='fund',
            name='claim_method',
            field=models.CharField(choices=[('A', 'Expense claim'), ('B', 'Invoice'), ('C', 'Combination of both')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='fund',
            name='payment_receiver',
            field=models.CharField(choices=[('A', 'Me (the fellow)'), ('B', 'Third party'), ('C', 'Combination of both')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='historicalfund',
            name='claim_method',
            field=models.CharField(choices=[('A', 'Expense claim'), ('B', 'Invoice'), ('C', 'Combination of both')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='historicalfund',
            name='payment_receiver',
            field=models.CharField(choices=[('A', 'Me (the fellow)'), ('B', 'Third party'), ('C', 'Combination of both')], default='A', max_length=1),
        ),
    ]