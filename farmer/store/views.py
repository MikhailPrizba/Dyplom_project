"""Этот модуль предоставляет представления и вспомогательные функции для
приложения магазина.

Классы:
     CommentCreateView: представление для создания нового комментария.
     CommentUpdateView: представление для обновления существующего комментария.
     CommentDeleteView: представление для удаления комментария.
     Search: представление для поиска продуктов.

Функции:
     sellerprofile: представление для отображения страницы профиля продавца.
     rating: вид для оценки продавца.
"""

from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import (HttpRequest, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from users.models import Buyer, Ratings, Seller

from .models import Category, Comment, Product


def home(request: HttpRequest, category_slug=None) -> HttpResponse:
    """Представление главной страницы."""
    category = None
    categories = Category.objects.all()
    # Фильтрация продуктов в зависимости от группы пользователя.
    if request.user.groups.filter(name="Sellers").exists():
        products = Product.objects.filter(seller=request.user)
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


def product_detail(request: HttpRequest, slug: str, id: int) -> HttpResponse:
    """Представление для страницы продукта."""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # Форма для добавления продукта в корзину
    cart_product_form = CartAddProductForm()
    comments = product.comment_set.all()
    if request.user.groups.filter(name="Sellers").exists():
        return render(
            request,
            "store/products/seller_product_detail.html",
            {
                "product": product,
                "comments": comments,
            },
        )
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


@login_required(login_url="users:login")
@require_POST
def product_like(request: HttpRequest) -> JsonResponse:
    """Добавление/удаление лайка продукта."""
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


class CommentCreateView(CreateView):
    """Отображает форму создания комментария."""

    model = Comment
    fields = ["text"]

    def form_valid(self, form) -> HttpResponse:
        """Сохраняет комментарий, привязывая его к пользователю и продукту, и
        возвращает HTTP-ответ."""

        # Получаем значения slug и id из kwargs и используем их для связи с продуктом
        form.instance.product = Product.objects.get(
            slug=self.kwargs["slug"], id=self.kwargs["id"]
        )

        # Сохраняем пользователя
        form.instance.user = User.objects.get(id=self.request.user.id)

        return super().form_valid(form)


class CommentUpdateView(UpdateView):
    """Отображает форму редактирования комментария."""

    model = Comment
    fields = ["text"]


class CommentDeleteView(DeleteView):
    """Отображает форму удаления комментария."""

    model = Comment

    def get_success_url(self, **kwargs) -> str:
        """Возвращает URL для перенаправления после успешного удаления
        комментария."""

        return reverse_lazy(
            "store:product_detail",
            kwargs={"slug": self.object.product.slug,
                    "id": self.object.product.id},
        )


@login_required(login_url="users:login")
def sellerprofile(request: HttpRequest, id: int) -> HttpResponse:
    """Отображает страницу профиля продавца."""

    user = get_object_or_404(User, id=id)

    profile = user.seller
    products = user.seller_products.all()

    return render(
        request,
        "store/profile/seller_profile.html",
        {"profile": profile, "products": products},
    )


@login_required(login_url="users:login")
@require_POST
def rating(request: HttpRequest) -> JsonResponse:
    """Обрабатывает POST-запрос с рейтингом и идентификатором продавца и
    сохраняет рейтинг.

    Возвращает JSON-ответ, указывающий на успех операции.
    """

    rating_num = request.POST.get("rating")
    seller_id = request.POST.get("seller_id")

    if rating_num and seller_id:
        seller = get_object_or_404(Seller, id=seller_id)

        rating, create = Ratings.objects.get_or_create(
            buyer=request.user.buyer, seller=seller
        )

        if rating.rating == 0:
            rating.rating = rating_num
            rating.save()

        return JsonResponse({"success": True})

    # Если что-то пошло не так, возвращаем ошибку
    return JsonResponse({"status": "error"})


class Search(ListView):
    """Отображает результаты поиска продуктов.

    Если по запросу ничего не найдено, перенаправляет на главную
    страницу магазина.
    """

    template_name = "store/products/home.html"
    context_object_name = "products"

    def get_queryset(self):
        """Возвращает список продуктов, соответствующих поисковому запросу."""

        product = Product.objects.filter(
            name__icontains=self.request.GET.get("q"))

        return product

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет поисковый запрос в контекст шаблона."""

        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context

    def render_to_response(self, context, **response_kwargs):
        """Отображает ответ и перенаправляет на главную страницу магазина, если
        результаты поиска не найдены."""

        if not Search.get_queryset(self):
            return redirect("store:home")
        else:
            return super().render_to_response(context, **response_kwargs)
