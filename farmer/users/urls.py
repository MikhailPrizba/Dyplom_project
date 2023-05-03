from django.urls import path, reverse_lazy
from .views import register_buyer, register_seller, profile, edit
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


app_name = 'users'
urlpatterns = [
    path('seller/register/', register_seller, name='seller_register'),
    path('buyer/register/', register_buyer, name='buyer_register'),
    path('login/', LoginView.as_view(template_name='users/registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/registration/logout.html'), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='users/registration/change_password.html'), name='change_password'),
    path('change-password_done/', PasswordChangeDoneView.as_view(
        template_name='change_password_done.html'), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(template_name='users/registration/password_reset.html',
         email_template_name='users/registration/password_reset_email.html', success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='users/registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/registration/password_reset_confirm.html',
         success_url=reverse_lazy("users:password_reset_complete")), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='users/registration/password_reset_complete.html',), name='password_reset_complete'),
    path('profile/', profile, name='profile'),
    path('edit/', edit, name='edit'),


]
