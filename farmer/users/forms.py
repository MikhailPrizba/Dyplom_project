from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Seller, Buyer


class SellerForm(UserCreationForm):

    photo = forms.ImageField(required=False)
    address = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=20, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        user.save()
        seller = Seller.objects.create(
            user=user,
            photo=self.cleaned_data['photo'],
            address=self.cleaned_data['address'],
            phone_number=self.cleaned_data['phone_number']
        )
        # создаем объект Seller и привязываем его к пользователю
        if commit:
            seller.save()
        return user


class BuyerForm(UserCreationForm):

    phone_number = forms.CharField(max_length=20, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_buyer = True
        user.save()
        buyer = Buyer.objects.create(
            user=user,
            phone_number=self.cleaned_data['phone_number']
        )
        # создаем объект Seller и привязываем его к пользователю
        if commit:
            buyer.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class BuyerEditForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['phone_number']

class SellerEditForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['photo', 'address', 'phone_number']