# Generated by Django 4.2 on 2023-05-10 22:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_remove_seller_house_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="seller",
            name="house_number",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
