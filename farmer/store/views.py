from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .models import Product, Category, Comment
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from cart.forms import CartAddProductForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


def home(request: HttpRequest, category_slug=None):
    category = None
    categories = Category.objects.all()

    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'store/products/home.html',
                  {'categories': categories,
                   'products': products,
                   'category': category})


def product_detail(request: HttpRequest, slug, id, ):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    comments = product.comment_set.all()
    return render(request,
                  'store/products/product_detail.html',
                  {'product': product, 'cart_product_form': cart_product_form, 'comments':comments},
                  )
@login_required
@require_POST
def product_like(request):
     
    product_id = request.POST.get('id')
    action = request.POST.get('action')
    if product_id and action:
        try:
            product = Product.objects.get(id=product_id)
            if action == 'like':
                product.users_like.add(request.user)
                
            else:
                product.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except product.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

class CommentCreateView(CreateView): #создание комментариев
    model = Comment
    fields = ['text']

    def form_valid(self, form) -> HttpResponse:
        print(self.kwargs)
        form.instance.product = Product.objects.get(slug = self.kwargs['slug'], id = self.kwargs['id'])
        form.instance.user = User.objects.get(id = self.request.user.id)
        
        return super().form_valid(form)
class CommentUpdateView(UpdateView): 
    model = Comment
    fields = ['text']

class CommentDeleteView(DeleteView):
    model = Comment
    def get_success_url(self, **kwargs) -> str:
        return reverse_lazy('store:product_detail', kwargs={'slug':self.object.product.slug, 'id' :self.object.product.id})

