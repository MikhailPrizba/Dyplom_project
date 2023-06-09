# Generated by Django 4.2 on 2023-05-03 22:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
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
                ("text", models.TextField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.product"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["product"], name="store_comme_product_65ca19_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["user"], name="store_comme_user_id_788131_idx"),
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(fields=["active"],
                               name="store_comme_active_b586b8_idx"),
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["created_at"], name="store_comme_created_88cd25_idx"
            ),
        ),
    ]
