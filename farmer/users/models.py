from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class Seller(models.Model):
    user: models.OneToOneField[User] = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    photo: models.ImageField = models.ImageField(upload_to="sellers/", blank=True)
    address: models.CharField = models.CharField(max_length=100, blank=True)
    phone_number: models.CharField = models.CharField(max_length=20, blank=True)
    is_seller: models.BooleanField = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.username
    
    def get_average_rating(self) -> float:
        ratings = Ratings.objects.filter(
            seller=self).aggregate(Avg("rating"))
        return round((ratings["rating__avg"]/2), 1)



class Buyer(models.Model):
    user: models.OneToOneField[User] = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    phone_number: models.CharField = models.CharField(max_length=20)
    is_buyer: models.BooleanField = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.username


class Ratings(models.Model):
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

    

