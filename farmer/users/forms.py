"""Этот модуль предоставляет формы для создания и обновления профилей
пользователей, которые используются как покупателями, так и продавцами.

Классы:
- SellerForm: Форма для создания пользователя с ролью продавца.
- BuyerForm: Форма для создания пользователя с ролью покупателя.
- UserEditForm: Форма для редактирования профиля пользователя.
- BuyerEditForm: Форма для редактирования профиля покупателя.
- SellerEditForm: Форма для редактирования профиля продавца.
"""


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import Buyer, Seller
from .authentication import is_real_address

class SellerForm(UserCreationForm):
    """Форма для регистрации продавца."""

    photo: forms.ImageField = forms.ImageField(required=False)
    country: forms.CharField = forms.CharField(max_length=100, required=True)
    phone_number: forms.CharField = forms.CharField(
        max_length=20, required=True)
    city: forms.CharField = forms.CharField(max_length=100, required=True)
    
    address: forms.CharField = forms.CharField(max_length=100, required=True)
    house_number : forms.CharField = forms.CharField(max_length=100, required=True)
    


    class Meta(UserCreationForm.Meta):
        model: type = User
        fields: tuple[str] = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self) -> str:
        """Проверяет уникальность адреса электронной почты, введенной в форму.

        Если адрес уже используется в другой учетной записи,
        генерируется исключение
        """
        data: str = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data
    
    
    
    
    def clean_house_number(self) -> str:
        """Проверяет существование адреса, в
        введенной в форму
        """
        
        address = self.cleaned_data["address"]
        city = self.cleaned_data["city"]
        house_number = self.cleaned_data["house_number"]
        country = self.cleaned_data["country"]
        
        address_all = f" {house_number}/{address} {city} {country}  "
        
        
        if not is_real_address(address_all):
            raise forms.ValidationError("Введите реальный адрес.")
        return address_all

    def save(self, commit: bool = True) -> User:
        """Создает объект Seller и привязывает его."""
        user: User = super().save(commit=False)
        user.is_seller = True
        with transaction.atomic():
            user.save()
            seller: Seller = Seller.objects.create(
                user=user,
                photo=self.cleaned_data["photo"],
                country=self.cleaned_data["country"],
                city=self.cleaned_data["city"],
                address=self.cleaned_data["address"],
                house_number=self.cleaned_data["house_number"],
                
                phone_number=self.cleaned_data["phone_number"],
            )

            
            # создаем объект Seller и привязываем его к пользователю
            
            if commit:
                seller.save()
        return user


class BuyerForm(UserCreationForm):
    """Форма для регистрации покупателя."""

    phone_number: forms.CharField = forms.CharField(
        max_length=20, required=True)

    class Meta(UserCreationForm.Meta):
        model: type = User
        fields: tuple[str] = ("username", "email", "password1", "password2")

    def clean_email(self) -> str:
        """Проверяет уникальность адреса электронной почты, введенной в форму.

        Если адрес уже используется в другой учетной записи,
        генерируется исключение
        """
        data: str = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data

    def save(self, commit: bool = True) -> User:
        """Создает объект Buyer и привязывает его."""
        user: User = super().save(commit=False)
        with transaction.atomic():
            user.is_buyer = True
            user.save()
            buyer: Buyer = Buyer.objects.create(
                user=user, phone_number=self.cleaned_data["phone_number"]
            )
            # создаем объект Buyer и привязываем его к пользователю
            if commit:
                buyer.save()
        return user


class UserEditForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя."""

    class Meta:
        model: type = User
        fields: list[str] = ["first_name", "last_name", "email"]


class BuyerEditForm(forms.ModelForm):
    """Форма для редактирования профиля покупателя."""

    class Meta:
        model: type = Buyer
        fields: list[str] = ["phone_number"]


class SellerEditForm(forms.ModelForm):
    """Форма для редактирования профиля продавца."""

    class Meta:
        model: type = Seller
        fields: list[str] = ["photo", "house_number", "phone_number"]

    