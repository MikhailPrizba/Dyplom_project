from django.urls import path
from .views import register
from django.contrib.auth.views import LoginView,LogoutView, PasswordChangeView

app_name = 'users'
urlpatterns = [
    path('seller/register/', register, name='seller_register'),
    
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('change_password/', PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    
]