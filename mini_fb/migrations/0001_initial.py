# Generated by Django 5.1.1 on 2024-10-07 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("image_url", models.URLField(blank=True)),

            ],
        ),
    ]
