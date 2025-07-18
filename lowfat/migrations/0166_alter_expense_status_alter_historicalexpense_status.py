# Generated by Django 4.2 on 2025-06-23 04:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lowfat", "0165_alter_claimant_mastodon_instance_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="status",
            field=models.CharField(
                choices=[
                    ("S", "Submitted"),
                    ("P", "Processing"),
                    ("A", "Approved"),
                    ("R", "Rejected"),
                    ("C", "Cancelled"),
                    ("X", "Removed"),
                ],
                default="S",
                max_length=1,
            ),
        ),
        migrations.AlterField(
            model_name="historicalexpense",
            name="status",
            field=models.CharField(
                choices=[
                    ("S", "Submitted"),
                    ("P", "Processing"),
                    ("A", "Approved"),
                    ("R", "Rejected"),
                    ("C", "Cancelled"),
                    ("X", "Removed"),
                ],
                default="S",
                max_length=1,
            ),
        ),
    ]
