from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
# class Store(models.Model):
#     name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    image_url = models.CharField(max_length=200, null=True, blank=True)
    # store = models.ForeignKey(Store, related_name='products')
    store = models.CharField(max_length=50)
    category = models.CharField(max_length=50, null=True, blank=True)


class Customer(models.Model):
    user = models.OneToOneField(User, related_name='customer', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class Favorite(models.Model):
    product = models.ForeignKey(Product, related_name='favorites', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='favorites', on_delete=models.CASCADE)
    list_name = models.CharField(max_length=50, default='Favorites')