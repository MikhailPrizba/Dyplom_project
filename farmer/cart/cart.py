from decimal import Decimal
from typing import Dict, List, Union

from django.conf import settings
from django.http.request import HttpRequest

from store.models import Product


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        """
        Инициализация корзины..
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart: Dict[str, Union[int, str, Product]] = cart

    def __iter__(self) -> List[Dict[str, Union[str, Decimal, Product]]]:
        """
        Итерация по элементам в корзине и получение продуктов из базы данных.
        """

        product_ids = self.cart.keys()
        # получение объектов продуктов и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self) -> int:
        """
        Подсчет количества элементов в корзине.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def add(
        self, product: Product, quantity: int = 1, override_quantity: bool = False
    ) -> None:
        """
        Добавление продукта в корзину или обновление его количества.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self) -> None:
        # отметить сессию как "измененную", чтобы убедиться, что она будет сохранена
        self.session.modified = True

    def remove(self, product: Product) -> None:
        """
        Удаление продукта из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self) -> None:
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self) -> Decimal:
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )
