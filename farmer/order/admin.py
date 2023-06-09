from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Класс для создания встроенной админки для модели OrderItem."""

    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Класс для создания админки для модели Order."""

    list_display = [
        "id",
        "user",
        "first_name",
        "last_name",
        "email",
        "address",
        "city",
        "paid",
        "created",
        "updated",
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
