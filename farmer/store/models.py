from typing import Optional

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категория товара."""

    name: str = models.CharField(max_length=100)
    slug: str = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural: str = "Categories"
        verbose_name: str = "Category"
        ordering: list = ["name"]
        indexes: list = [
            models.Index(fields=["name"]),
        ]

    def get_absolute_url(self) -> str:
        """Метод для получения URL страницы списка товаров, относящихся к
        данной категории."""
        return reverse("store:product_list_by_category", args=[self.slug])

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Товар в магазине."""

    category: Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller: User = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        editable=False,
        related_name="seller_products",
    )
    name: str = models.CharField(max_length=100)
    price: float = models.DecimalField(max_digits=10, decimal_places=2)
    slug: str = models.SlugField(max_length=100)
    description: Optional[str] = models.TextField(blank=True, null=True)
    image: Optional[models.ImageField] = models.ImageField(
        upload_to="images/products/", blank=True, null=True
    )
    available: bool = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    users_like: models.ManyToManyField = models.ManyToManyField(
        User, related_name="products_liked", blank=True, editable=False
    )
    total_likes: int = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering: list = ["name"]
        verbose_name_plural: str = "Products"
        verbose_name: str = "Product"
        indexes: list = [
            models.Index(fields=["name"]),
            models.Index(fields=["id", "slug"]),
        ]

    def save(self, *args, **kwargs) -> None:
        """Переопределение метода сохранения объекта.

        Если это новый объект, то устанавливает продавца товара из
        переданных параметров или текущего пользователя.
        """
        if not self.pk:
            self.seller = (
                self.seller or kwargs.pop(
                    "seller", None) or User.objects.get(pk=1)
            )
            # попытаться установить `seller` из self.seller или из переданных kwargs
            # если не установлено, установить текущего пользователя, который создал продукт
            super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Метод для получения URL страницы с подробной информацией о
        товаре."""
        return reverse("store:product_detail", args=[self.slug, self.id])

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    """Комментарий к товару."""

    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    text: str = models.TextField(max_length=200)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    active: bool = models.BooleanField(default=True)

    class Meta:
        ordering: list = ["-created_at"]
        indexes: list = [
            models.Index(fields=["product"]),
            models.Index(fields=["user"]),
            models.Index(fields=["active"]),
            models.Index(fields=["created_at"]),
        ]

    def get_absolute_url(self) -> str:
        """Метод для получения URL страницы с подробной информацией о
        товаре."""
        return reverse(
            "store:product_detail", args=[self.product.slug, self.product.id]
        )

    def __str__(self) -> str:
        return f"{self.user.username} - {self.product.name}"
