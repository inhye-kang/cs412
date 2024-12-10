# Generated by Django 5.1.3 on 2024-12-09 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0007_alter_userprofile_city_alter_userprofile_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="image_url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.PositiveIntegerField(),
        ),
    ]
