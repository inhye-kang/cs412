# Generated by Django 5.1.2 on 2024-12-09 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0017_remove_wine_country_wine_country_of_origin"),
    ]

    operations = [
        migrations.DeleteModel(
            name="WineRanking",
        ),
    ]