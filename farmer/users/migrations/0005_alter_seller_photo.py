# Generated by Django 4.2 on 2023-05-09 20:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_seller_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seller",
            name="photo",
            field=models.ImageField(blank=True, upload_to="images/seller_photos/"),
        ),
    ]