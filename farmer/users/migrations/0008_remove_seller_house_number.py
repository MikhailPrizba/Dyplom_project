# Generated by Django 4.2 on 2023-05-10 20:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_seller_house_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="seller",
            name="house_number",
        ),
    ]
