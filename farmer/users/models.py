"""Модуль содержит модели Django для создания профилей продавца и покупателя, а
также модель для хранения рейтинга пользователя.

Классы:
- Seller: модель профиля продавца.
- Buyer: модель покупателя.
- Ratings: модель рейтинга пользователя.
"""
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
import requests
from django.core.exceptions import ValidationError


class Seller(models.Model):
    """Модель профиля продавца."""
    user: models.OneToOneField[User] = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    photo: models.ImageField = models.ImageField(upload_to="images/seller_photos/", blank=True)
    country : models.CharField = models.CharField(max_length=100, blank=True)
    city : models.CharField = models.CharField(max_length=100, blank=True)
    address: models.CharField = models.CharField(max_length=100, blank=True)
    house_number: models.CharField = models.CharField(max_length=100, blank=True)
    phone_number: models.CharField = models.CharField(max_length=20, blank=True)
    is_seller: models.BooleanField = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.username
    
    def get_average_rating(self) -> float:
        """Возвращает среднюю оценку продавца."""
        ratings = Ratings.objects.filter(
            seller=self).aggregate(Avg("rating"))
        return round((ratings["rating__avg"]/2), 1)


    def get_real_address(self):
        url = 'https://nominatim.openstreetmap.org/search/'
        address = f" {self.house_number}/{self.address} {self.city} {self.country}"
        params = {
            'q': address,
            'format': 'json',
        }
        response = requests.get(url, params=params)
        data = response.json()
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        
        return (lat, lon)
    
class Buyer(models.Model):
    """Модель профиля покупателя."""
    user: models.OneToOneField[User] = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    phone_number: models.CharField = models.CharField(max_length=20)
    is_buyer: models.BooleanField = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.username


class Ratings(models.Model):
    """Модель рейтинга пользователя."""
    seller: models.ForeignKey[Seller] = models.ForeignKey(
        Seller, on_delete=models.CASCADE
    )
    buyer: models.ForeignKey[Buyer] = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    rating: models.IntegerField = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ],
    )

    class Meta:
        unique_together = (("seller", "buyer"),)


