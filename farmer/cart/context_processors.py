from django.http import HttpRequest

from .cart import Cart


def cart(request: HttpRequest) -> dict[str, Cart]:
    """Добавляет объект Cart в контекст запроса для доступа ко всем
    шаблонам."""
    return {"cart": Cart(request)}
