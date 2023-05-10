from typing import Union

from django.contrib.auth.models import User
from django.http import HttpRequest
import requests
from django.core.exceptions import ValidationError


class EmailAuthBackend:
    """Аутентификационный backend, который позволяет пользователям войти в
    систему с помощью их электронной почты и пароля."""

    def authenticate(
        self, request: HttpRequest, username: str = None, password: str = None
    ) -> Union[User, None]:
        """Аутентификация пользователя по электронной почте и паролю.

        Возвращает пользователя, если электронная почта и пароль
        совпадают, в противном случае возвращает None.
        """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id: int) -> Union[User, None]:
        """Возвращает пользователя по его идентификатору."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None











def is_real_address(address: str) -> bool:
    url = 'https://nominatim.openstreetmap.org/search/'
    params = {
        'q': address,
        'format': 'json',
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    if not data:
        return False

    return True