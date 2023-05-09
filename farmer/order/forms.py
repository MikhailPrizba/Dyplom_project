from django import forms

from .models import Order


class OrderCreationForm(forms.ModelForm):
    """Форма для создания нового заказа."""

    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "email",
            "address",
            "city",
        ]
