from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Seller, Buyer, CustomUser

class SellerRegistrationForm(UserCreationForm):
    nickname = forms.CharField(max_length=50)
    geolocation = forms.CharField(max_length=100)
    rating = forms.FloatField()
    photo = forms.ImageField()
    phone_number = forms.CharField(max_length=20)
    class Meta:
        model = Seller
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'nickname', 'geolocation','rating', 'photo', 'phone_number']

class BuyerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20)
    class Meta:
        model = Buyer
        fields = ['username', 'first_name', 'last_name', 'email','phone_number', 'password1', 'password2']

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')