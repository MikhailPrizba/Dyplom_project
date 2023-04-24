from django.db import models
from django.contrib.auth.models import AbstractUser, Permission,Group

class CustomUser(AbstractUser):
    pass
class Seller(AbstractUser):
    nickname = models.CharField(max_length=50)
    geolocation = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    rating = models.FloatField()
    photo = models.ImageField(upload_to='seller_photos/', blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="%(class)s_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="%(class)s_permissions")

    def add_product(self, product_name, price, description):
        # implement logic to add a new product to the seller's inventory
        pass

    def remove_product(self, product_id):
        # implement logic to remove a product from the seller's inventory
        pass

    def update_product(self, product_id, product_name, price, description):
        # implement logic to update an existing product in the seller's inventory
        pass

    class Meta:
        verbose_name ='Seller'
        verbose_name_plural = 'Sellers'
class Buyer(AbstractUser):
    phone_number = models.CharField(max_length=20)
    groups = models.ManyToManyField(Group, related_name="%(class)s_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="%(class)s_permissions")
    class Meta:
        verbose_name ='Buyer'
        verbose_name_plural = 'Byuers'
