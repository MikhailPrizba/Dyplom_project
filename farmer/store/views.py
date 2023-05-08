from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from cart.forms import CartAddProductForm
from users.models import Ratings, Seller, Buyer

from .models import Category, Comment, Product


# Представление главной страницы
def home(request: HttpRequest, category_slug=None) -> HttpResponse:
    category = None
    categories = Category.objects.all()
    if request.user.groups.filter(name="Sellers").exists():
        products = Product.objects.filter(seller = request.user)
    else:
        products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(
        request,
        "store/products/home.html",
        {"categories": categories, "products": products, "category": category},
    )


# Представление для страницы продукта
def product_detail(request: HttpRequest, slug: str, id: int) -> HttpResponse:
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # Форма для добавления продукта в корзину
    cart_product_form = CartAddProductForm()
    comments = product.comment_set.all()
    if request.user.groups.filter(name="Sellers").exists():
        return render(request,
        "store/products/seller_product_detail.html",
        {
            "product": product,
            
            "comments": comments,
        },)
    else:

        return render(
            request,
            "store/products/product_detail.html",
            {
                "product": product,
                "cart_product_form": cart_product_form,
                "comments": comments,
            },
        )


# Представление для добавления/удаления лайка продукт
@login_required
@require_POST
def product_like(request: HttpRequest) -> JsonResponse:
    # Получаем id продукта и действие (лайк или удаление лайка)
    product_id = request.POST.get("id")
    action = request.POST.get("action")
    # Если переданы оба параметра, то пытаемся найти продукт по id и выполнить действие
    if product_id and action:
        try:
            product = Product.objects.get(id=product_id)
            if action == "like":
                product.users_like.add(request.user)
            else:
                product.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except product.DoesNotExist:
            pass
    # Если что-то пошло не так, возвращаем ошибку
    return JsonResponse({"status": "error"})


# Создание комментария
class CommentCreateView(CreateView):
    model = Comment
    fields = ["text"]

    def form_valid(self, form) -> HttpResponse:
        print(self.kwargs)
        form.instance.product = Product.objects.get(
            slug=self.kwargs["slug"], id=self.kwargs["id"]
        )
        form.instance.user = User.objects.get(id=self.request.user.id)

        return super().form_valid(form)


# Обновление комментария
class CommentUpdateView(UpdateView):
    model = Comment
    fields = ["text"]


# Удаление комментария
class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self, **kwargs) -> str:
        return reverse_lazy(
            "store:product_detail",
            kwargs={"slug": self.object.product.slug, "id": self.object.product.id},
        )


# Отображение страницы продавца
@login_required
def sellerprofile(request: HttpRequest, id: int) -> HttpResponse:
    user = get_object_or_404(User, id=id)

    profile = user.seller
    products = user.seller_products.all()
    return render(
        request,
        "store/profile/seller_profile.html",
        {"profile": profile, "products": products},
    )


@login_required
@require_POST
def rating(request: HttpRequest) -> JsonResponse:
    
    rating_num = request.POST.get("rating")
    seller_id = request.POST.get("seller_id")
    if (rating_num and seller_id):
        
        seller = get_object_or_404(Seller, id=seller_id)

        rating = Ratings(buyer = request.user.buyer, rating = rating_num, seller =seller)
        print(dir(seller))
        if rating not in seller.ratings_set.all():
            rating.save()
        else:
            print('a')
            pass

        return JsonResponse({"success": True})
     # Если что-то пошло не так, возвращаем ошибку
    return JsonResponse({"status": "error"})

class Search(ListView):
    
    template_name = 'store/products/home.html'
    context_object_name = 'products'
    
    
    
    def get_queryset(self) :
        product = Product.objects.filter(name__icontains = self.request.GET.get('q'))
        
        return product
        
    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context
    def render_to_response(self, context, **response_kwargs):
        print(Search.get_queryset(self))
        if not Search.get_queryset(self):
            
            return redirect('store:home')
        else:
            return super().render_to_response(context, **response_kwargs)