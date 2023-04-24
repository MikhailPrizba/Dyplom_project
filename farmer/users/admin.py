from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Seller, Buyer

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = get_user_model()
    list_display = ['email', 'username', 'is_staff']

class SellerAdmin(admin.ModelAdmin):
    model = Seller
    verbose_name = 'Seller'
    verbose_name_plural = 'Sellers'
    # define other customizations for the Seller admin view here

class BuyerAdmin(admin.ModelAdmin):
    model = Buyer
    
    verbose_name_plural = 'Buyers'
    # define other customizations for the Buyer admin view here

admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Seller, SellerAdmin,)
admin.site.register(Buyer, BuyerAdmin)