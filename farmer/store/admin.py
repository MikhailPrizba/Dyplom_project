from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Регистрация категорий  в админке."""

    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Регистрация товара в админке."""

    list_display = ["name", "description", "price", "seller"]
    list_filter = ["seller"]
    search_fields = ["name", "description"]
    actions = ["delete_selected"]
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Возвращает набор запросов на основе роли пользователя."""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(seller=request.user)
        return qs

    def save_model(
        self, request: HttpRequest, obj: Product, form, change: bool
    ) -> None:
        """Сохраняет объект в базу данных.

        Если это новый объект
        """
        if not change:
            obj.seller = request.user
        super().save_model(request, obj, form, change)
