"""Модуль содержит два класса: Order и OrderItem.

Оба класса отвечают за моделирование данных, используемых в заказе
"""
from django.contrib.auth.models import User
from django.db import models
from store.models import Product


class Order(models.Model):
    """Создает модель заказа, сделанного пользователем в магазине."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> str:
        """Возвращает строковое представление заказа."""
        return f"Order {self.id}"

    def get_total_cost(self) -> float:
        """Метод для получения общей стоимости заказа.

        Суммирует стоимость всех позиций заказа.
        """
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Создает модель позиции заказа."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        """Возвращает строковое представление позиции заказа."""
        return f"{self.id}"

    def get_cost(self) -> float:
        """Метод для получения стоимости позиции заказа.

        Возвращает произведение цены на количество товара.
        """
        return self.price * self.quantity
