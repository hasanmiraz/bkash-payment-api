# Generated by Django 4.1.7 on 2023-02-18 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bkashAPI", "0003_rename_refreshtoken_granttokenmodel_id_token_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="refundModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("paymentID", models.TextField()),
                ("trxID", models.TextField()),
                ("refundTrxID", models.TextField()),
            ],
        ),
    ]
