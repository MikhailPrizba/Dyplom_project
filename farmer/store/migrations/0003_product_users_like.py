# Generated by Django 4.2 on 2023-05-05 01:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_comment_comment_store_comme_product_65ca19_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='products_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
