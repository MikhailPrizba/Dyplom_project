from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.utils import OperationalError,ProgrammingError
from store.models import Product
from users.models import Buyer, Seller

# Register your models here.


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    """Регистрация продавца в администраторе."""

    list_display: tuple = ("user", "phone_number", "address")
    list_filter: tuple = ("user", "phone_number", "address")


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    """Регистрация покупателя в администраторе."""

    list_display: tuple = ("user", "phone_number")


"""
создаем две группы пользователей: "Sellers" и "Buyers". Затем ищем 
разрешения для модели "Product" и сохраняет их в переменную "seller_permissions". 
Далее добавляем все найденные разрешения в группу "Sellers", чтобы пользователи 
этой группы могли выполнять действия, связанные с продуктами.
"""
try:
    content_type: ContentType = ContentType.objects.get_for_model(Product)
    seller_permissions: Permission = Permission.objects.filter(
        content_type=content_type)
    seller_group, created = Group.objects.get_or_create(name="Sellers")
    buyer_group, created = Group.objects.get_or_create(name="Buyers")
    seller_group.permissions.add(*seller_permissions)
except  (OperationalError, ProgrammingError):
    pass

