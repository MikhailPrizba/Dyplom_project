# Generated by Django 4.2 on 2023-05-07 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]