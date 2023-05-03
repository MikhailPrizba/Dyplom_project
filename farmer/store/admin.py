from django.contrib import admin
from .models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'seller']
    list_filter = ['seller']
    search_fields = ['name', 'description']
    actions = ['delete_selected']
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(seller=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.seller = request.user
        super().save_model(request, obj, form, change)


