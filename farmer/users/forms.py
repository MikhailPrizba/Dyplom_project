from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Buyer, Seller


class SellerForm(UserCreationForm):
    photo: forms.ImageField = forms.ImageField(required=False)
    address: forms.CharField = forms.CharField(max_length=100, required=True)
    phone_number: forms.CharField = forms.CharField(max_length=20, required=True)

    class Meta(UserCreationForm.Meta):
        model: type = User
        fields: tuple[str, str, str, str] = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self) -> str:
        data: str = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.is_seller = True
        user.save()
        seller: Seller = Seller.objects.create(
            user=user,
            photo=self.cleaned_data["photo"],
            address=self.cleaned_data["address"],
            phone_number=self.cleaned_data["phone_number"],
        )
        # создаем объект Seller и привязываем его к пользователю
        if commit:
            seller.save()
        return user


class BuyerForm(UserCreationForm):
    phone_number: forms.CharField = forms.CharField(max_length=20, required=True)

    class Meta(UserCreationForm.Meta):
        model: type = User
        fields: tuple[str] = ("username", "email", "password1", "password2")

    def clean_email(self) -> str:
        data: str = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.is_buyer = True
        user.save()
        buyer: Buyer = Buyer.objects.create(
            user=user, phone_number=self.cleaned_data["phone_number"]
        )
        # создаем объект Seller и привязываем его к пользователю
        if commit:
            buyer.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model: type = User
        fields: list[str] = ["first_name", "last_name", "email"]


class BuyerEditForm(forms.ModelForm):
    class Meta:
        model: type = Buyer
        fields: list[str] = ["phone_number"]


class SellerEditForm(forms.ModelForm):
    class Meta:
        model: type = Seller
        fields: list[str] = ["photo", "address", "phone_number"]
