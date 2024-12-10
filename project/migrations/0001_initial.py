# Generated by Django 5.1.3 on 2024-12-08 21:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Wine",
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
                ("name", models.CharField(max_length=200)),
                ("winery", models.CharField(blank=True, max_length=200, null=True)),
                ("category", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "designation",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("varietal", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "appellation",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("alcohol", models.FloatField(blank=True, null=True)),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("rating", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("reviewer", models.CharField(blank=True, max_length=100, null=True)),
                ("wine_review", models.TextField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
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
                ("first_name", models.TextField()),
                ("last_name", models.TextField()),
                ("email", models.TextField()),
                ("city", models.TextField()),
                ("image_url", models.URLField(blank=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TriedWine",
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
                ("tried_at", models.DateTimeField(auto_now_add=True)),
                ("location", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "picture",
                    models.ImageField(blank=True, null=True, upload_to="tried_wines/"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "wine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="project.wine"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
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
                ("review_text", models.TextField()),
                ("rating", models.PositiveSmallIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "wine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="project.wine",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Friendship",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "friend_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friendship_receiver",
                        to="project.userprofile",
                    ),
                ),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="friendship_creator",
                        to="project.userprofile",
                    ),
                ),
            ],
            options={
                "unique_together": {("user_profile", "friend_profile")},
            },
        ),
    ]