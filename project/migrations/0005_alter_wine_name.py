# Generated by Django 5.1.3 on 2024-12-09 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0004_userprofile_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wine",
            name="name",
            field=models.CharField(default="Wine Name", max_length=200),
        ),
    ]
