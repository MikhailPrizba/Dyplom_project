from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def get_absolute_url(self):
        return reverse("store:product_list_by_category", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, related_name='seller_products', )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='images/products/', blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(User, related_name='products_liked', blank=True,editable=False)
    total_likes = models.IntegerField(default=0,editable=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Products"
        verbose_name = "Product"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['id', 'slug']),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:  # если это новый объект
            self.seller = self.seller or kwargs.pop(
                'seller', None) or get_user_model().objects.get(pk=1)
            # попытаться установить `seller` из self.seller или из переданных kwargs
            # если не установлено, установить текущего пользователя, который создал продукт
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug, self.id])

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
            models.Index(fields=['active']),
            models.Index(fields=['created_at']),
        ]
    

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.product.slug, self.product.id])
        #return reverse("store:product_detail", args=[self.object.product.slug, self.object.product.id])

    def __str__(self) -> str:
        return f'{self.user.username} - {self.product.name}'