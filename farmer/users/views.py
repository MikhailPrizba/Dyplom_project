from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SellerRegistrationForm, BuyerRegistrationForm

def seller_registration(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_seller = True
            user.save()
            login(request, user)
            return redirect('store:home/')
    else:
        form = SellerRegistrationForm()
    return render(request, 'seller_registration.html', {'form': form})

def buyer_registration(request):
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_buyer = True
            user.save()
            login(request, user)
            return redirect('store: home')
    else:
        form = BuyerRegistrationForm()
    return render(request, 'buyer_registration.html', {'form': form})