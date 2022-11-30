# Generated by Django 4.1.3 on 2022-11-29 07:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("title", models.CharField(max_length=30)),
                ("start_at", models.DateTimeField()),
                ("end_at", models.DateTimeField()),
                ("goal", models.CharField(max_length=50)),
                ("skill", models.CharField(max_length=100)),
                ("functions", models.TextField()),
                ("leader", models.CharField(max_length=20)),
                (
                    "user",
                    models.ManyToManyField(
                        related_name="users", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]