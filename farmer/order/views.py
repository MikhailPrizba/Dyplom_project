from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from cart.cart import Cart

from .forms import OrderCreationForm
from .models import OrderItem
from .tasks import order_created


def order_create(request: HttpRequest) -> HttpResponse:
    """Функция создания заказа."""
    # Получаем объект корзины для текущего запроса
    cart = Cart(request)
    # Если метод запроса POST, создаем экземпляр OrderCreationForm с отправленными данными
    if request.method == "POST":
        form = OrderCreationForm(request.POST)
        # Проверяем валидность формы
        if form.is_valid():
            order = form.save()
            # Если пользователь аутентифицирован, связываем заказ с пользователем и сохраняем изменения
            if request.user.is_authenticated:
                order.user = request.user
                order.save()
            for item in cart:
                # Создаем объект OrderItem
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["price"],
                )
                # Обновляем корзину
            cart.clear()
            order_created.delay(order.id)
            return render(request, "orders/order/created.html", {"order": order})
    else:
        form = OrderCreationForm()
    return render(request, "orders/order/create.html", {"form": form, "cart": cart})
