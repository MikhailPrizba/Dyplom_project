from django.contrib import admin
from store.models import Product
from users.models import Seller, Buyer
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Register your models here.


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    list_filter = ('user', 'phone_number', 'address')


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('user',  'phone_number')


content_type = ContentType.objects.get_for_model(Product)
seller_permissions = Permission.objects.filter(content_type=content_type)


seller_group, created = Group.objects.get_or_create(name='Sellers')
buyer_group, created = Group.objects.get_or_create(name='Buyers')
seller_group.permissions.add(*seller_permissions)


