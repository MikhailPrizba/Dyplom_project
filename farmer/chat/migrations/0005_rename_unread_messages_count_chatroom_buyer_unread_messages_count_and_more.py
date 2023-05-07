# Generated by Django 4.2 on 2023-05-07 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_chatroom_unread_messages_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatroom',
            old_name='unread_messages_count',
            new_name='buyer_unread_messages_count',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='seller_unread_messages_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
