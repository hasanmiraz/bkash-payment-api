# Generated by Django 4.1.7 on 2023-02-14 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="agreement",
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
                ("agreementID", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="createPaymentID",
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
            ],
        ),
        migrations.CreateModel(
            name="grantToken",
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
                ("token", models.TextField()),
                ("refreshToken", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="successPayment",
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
            ],
        ),
    ]
