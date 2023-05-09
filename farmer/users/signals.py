from django.contrib.auth.models import Group, Permission, User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def assign_group(sender: object, instance: User, created: bool, **kwargs: dict) -> None:
    """Функция assign_group назначает новому пользователю определенную группу
    (Group) в зависимости от значения атрибутов is_seller и is_buyer.

    Если is_seller равен True, пользователю назначается группа
    "Sellers", а также ему присваиваются права доступа, связанные с этой
    группой. Если is_buyer равен True, пользователю назначается группа
    "Buyers".
    """
    if created:
        if hasattr(instance, "is_seller") and instance.is_seller:
            seller_group = Group.objects.get(name="Sellers")
            instance.groups.add(seller_group)
            seller_permissions = Permission.objects.filter(group=1)
            instance.user_permissions.add(*seller_permissions)
            instance.is_staff = True  # добавляем в администратора
            instance.save()
        elif hasattr(instance, "is_buyer") and instance.is_buyer:
            buyer_group = Group.objects.get(name="Buyers")
            instance.groups.add(buyer_group)
