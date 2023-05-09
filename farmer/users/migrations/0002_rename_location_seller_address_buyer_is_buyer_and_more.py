# Generated by Django 4.2 on 2023-05-03 22:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="seller",
            old_name="location",
            new_name="address",
        ),
        migrations.AddField(
            model_name="buyer",
            name="is_buyer",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="seller",
            name="is_seller",
            field=models.BooleanField(default=True),
        ),
    ]
