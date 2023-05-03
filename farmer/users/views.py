from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Seller, Buyer


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            user_type = request.POST.get('user_type')
            if user_type == 'seller':
                Seller.objects.create(user=user, photo=request.POST.get('photo'), location=request.POST.get('location'))
            elif user_type == 'buyer':
                Buyer.objects.create(user=user, shipping_address=request.POST.get('shipping_address'), billing_address=request.POST.get('billing_address'))
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})