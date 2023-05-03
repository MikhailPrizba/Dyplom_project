from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission


@receiver(post_save, sender=User)
def assign_group(sender, instance, created, **kwargs):

    if created:
        if hasattr(instance, 'is_seller') and instance.is_seller:
            seller_group = Group.objects.get(name='Sellers')
            instance.groups.add(seller_group)
            seller_permissions = Permission.objects.filter(group=1)
            instance.user_permissions.add(*seller_permissions)
            instance.is_staff = True
            instance.save()
        elif hasattr(instance, 'is_buyer') and instance.is_buyer:
            buyer_group = Group.objects.get(name='Buyers')
            instance.groups.add(buyer_group)
