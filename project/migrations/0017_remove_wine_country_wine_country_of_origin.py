# Generated by Django 5.1.2 on 2024-12-09 06:41

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0016_wineranking"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wine",
            name="country",
        ),
        migrations.AddField(
            model_name="wine",
            name="country_of_origin",
            field=django_countries.fields.CountryField(
                blank=True, max_length=2, null=True
            ),
        ),
    ]
