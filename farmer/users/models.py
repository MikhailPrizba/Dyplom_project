from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='sellers/', blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_seller = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    is_buyer = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class Ratings(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0),])

    class Meta:
        unique_together = (('seller', 'buyer'),)
    
    def get_average_rating(self):
        ratings = Ratings.objects.filter(seller=self.seller, buyer=self.buyer).aggregate(Avg('rating'))
        return ratings['rating__avg']
    