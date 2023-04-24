from django.db import models
from users.models import Seller
from django.urls import reverse
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
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/products/', blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Products"
        verbose_name = "Product"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['id', 'slug']),
        ]

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug, self.id])

    def __str__(self):
        return self.name