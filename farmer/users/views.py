"""Этот модуль предоставляет функциональные возможности, связанные с
регистрацией пользователей, профилем и редактированием.

Функции:

    register_seller регистрация продавца
    register_buyer регистрация покупателя
    edit редактирование профиля
    profile отображение профиля пользователя
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from order.models import Order
from store.models import Product

from .forms import (BuyerEditForm, BuyerForm, SellerEditForm, SellerForm,
                    UserEditForm)
from .models import Buyer, Seller


def register_seller(request: HttpRequest) -> HttpResponse:
    """Регистрация продавца."""
    if request.method == "POST":
        form = SellerForm(request.POST, files = request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("users:login")
    else:
        form = SellerForm()
    return render(request, "users/registration/register_seller.html", {"form": form})


def register_buyer(request: HttpRequest) -> HttpResponse:
    """Регистрация покупателя."""
    if request.method == "POST":
        form = BuyerForm(request.POST, files = request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("users:login")
    else:
        form = BuyerForm()
    return render(request, "users/registration/register_buyer.html", {"form": form})


@login_required(login_url="users:login")
def edit(request: HttpRequest) -> HttpResponse:
    """Редактирование профиля."""
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if request.user.is_staff:
            profile_form = SellerEditForm(
                instance=request.user.seller, data=request.POST, files=request.FILES
            )
        else:
            profile_form = BuyerEditForm(
                instance=request.user.buyer, data=request.POST, files=request.FILES
            )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Account updated!")
            return redirect("users:profile")

    else:
        user_form = UserEditForm(instance=request.user)
        if request.user.is_staff:
            profile_form = SellerEditForm(instance=request.user.seller)
        else:
            profile_form = BuyerEditForm(instance=request.user.buyer)
    return render(
        request,
        "users/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required(login_url="users:login")
def profile(request: HttpRequest) -> HttpResponse:
    """Профиль пользователя."""
    if request.user.groups.filter(name="Sellers").exists():
        profile = Seller.objects.get(user=request.user)
        products = Product.objects.filter(seller=request.user)
        context = {"profile": profile, "products": products}

    else:
        profile = Buyer.objects.get(user=request.user)
        orders = Order.objects.filter(user=request.user)

        like = Product.objects.filter(users_like=request.user)

        context = {"profile": profile, "orders": orders, "like": like}

    return render(
        request,
        "users/profile.html",
        context,
    )
