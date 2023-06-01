from django.urls import reverse
from django.shortcuts import redirect

class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == reverse('users:login'):
            return redirect('store:home') # Замените 'home' на URL-адрес страницы, на которую нужно перенаправлять авторизованных пользователей
        response = self.get_response(request)
        return response


class RegistrationRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and (request.path in [reverse('users:seller_register'), reverse('users:buyer_register')]):
            return redirect('store:home') # Замените 'home' на URL-адрес страницы, на которую нужно перенаправлять авторизованных пользователей
        response = self.get_response(request)
        return response
