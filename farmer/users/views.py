from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SellerForm, BuyerForm, BuyerEditForm, SellerEditForm, UserEditForm
from.models import Seller, Buyer
from order.models import Order, OrderItem


def register_seller(request):
    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('users:login')
    else:
        form = SellerForm()
    return render(request, 'users/registration/register_seller.html', {'form': form})


def register_buyer(request):
    if request.method == 'POST':
        form = BuyerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('users:login')
    else:
        form = BuyerForm()
    return render(request, 'users/registration/register_buyer.html', {'form': form})





@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                data=request.POST)
        if request.user.is_staff:
            profile_form = SellerEditForm(
                                    instance=request.user.seller,
                                    data=request.POST,
                                    files=request.FILES)
        else:
            profile_form = BuyerEditForm(
                                    instance=request.user.buyer,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Account updated!')
            return redirect('users:profile')
            
    else:
        user_form = UserEditForm(instance=request.user)
        if request.user.is_staff:
            profile_form = SellerEditForm(
                                    instance=request.user.seller)
        else:
            profile_form = BuyerEditForm(
                                    instance=request.user.buyer)
    return render(request,
                    'users/edit.html',
                    {'user_form': user_form,
                    'profile_form': profile_form})




@login_required(login_url='users:login')
def profile(request):
    
    if request.user.is_staff:
        profile = Seller.objects.get(user=request.user)
        context = {'profile': profile}
    else:
        profile = Buyer.objects.get(user=request.user)
        orders = Order.objects.filter(user=request.user)
        context = {'profile': profile, 'orders': orders}

    return render(request, 'users/profile.html', context)