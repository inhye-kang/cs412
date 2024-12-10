# Generated by Django 5.1.2 on 2024-12-09 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0014_review_varietal"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]