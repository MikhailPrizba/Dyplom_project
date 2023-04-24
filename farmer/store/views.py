from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .models import Product, Category
# Create your views here.
def home(request: HttpRequest, category_slug = None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available = True)
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = products.filter(category = category)
    
    return render(request, 
                  'store/products/home.html', 
                  {'categories': categories,
                    'products': products,
                    'category': category})

def product_detail(request: HttpRequest, slug,id, ):
    product = get_object_or_404(Product, id = id, slug = slug, available = True)
    return render(request, 
                  'store/products/product_detail.html', 
                  {'product': product})