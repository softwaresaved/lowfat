# Generated by Django 4.2 on 2024-08-30 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lowfat', '0160_alter_claimant_application_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimant',
            name='supplier_number',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='historicalclaimant',
            name='supplier_number',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
