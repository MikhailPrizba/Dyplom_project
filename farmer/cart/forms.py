from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductForm(forms.Form):
    # Определение поля формы, которое отвечает за количество товара.
    quantity: forms.TypedChoiceField = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int
    )
    # Определение поля формы, которое отвечает за возможность перезаписи количества товара.
    override: forms.BooleanField = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
