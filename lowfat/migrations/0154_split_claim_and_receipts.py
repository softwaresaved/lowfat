# Generated by Django 3.2.7 on 2022-06-09 14:34

from django.db import migrations, models
import lowfat.validator


class Migration(migrations.Migration):

    dependencies = [
        ('lowfat', '0153_update_default_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='receipts',
            field=models.FileField(null=True, upload_to='expenses/', validators=[lowfat.validator.pdf]),
        ),
        migrations.AddField(
            model_name='historicalexpense',
            name='receipts',
            field=models.TextField(max_length=100, null=True, validators=[lowfat.validator.pdf]),
        ),
        migrations.AlterField(
            model_name='expense',
            name='claim',
            field=models.FileField(upload_to='expenses/', validators=[lowfat.validator.validate_document]),
        ),
        migrations.AlterField(
            model_name='historicalexpense',
            name='claim',
            field=models.TextField(max_length=100, validators=[lowfat.validator.validate_document]),
        ),
    ]
