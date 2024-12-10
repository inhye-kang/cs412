# Generated by Django 5.1.2 on 2024-12-09 03:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0010_remove_review_wine_review_country_of_origin_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="price",
        ),
        migrations.RemoveField(
            model_name="review",
            name="varietal",
        ),
        migrations.RemoveField(
            model_name="review",
            name="wine_name",
        ),
        migrations.RemoveField(
            model_name="review",
            name="winery",
        ),
        migrations.AddField(
            model_name="review",
            name="wine",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="project.wine",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="body_rating",
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name="review",
            name="finish_rating",
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name="review",
            name="taste_rating",
            field=models.IntegerField(default=5),
        ),
    ]