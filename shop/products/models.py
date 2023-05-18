from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    info = models.TextField(null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, unique=False)
    image_url = models.CharField(max_length=255, unique=True)
    price = models.FloatField(null=False, blank=False, default=0.0)
    time_created = models.DateTimeField(auto_now=True)

    quantity = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-time_created']
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    class PaidStatus(models.TextChoices):
        PAID = 'Paid'
        IN_CART = 'In cart'
        
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    paid_status = models.CharField(max_length=7, choices=PaidStatus.choices, default=PaidStatus.IN_CART)
        
        
class Card(models.Model):
    number = models.CharField(max_length=16)
    validity_period = models.CharField(max_length=5, default='01/00')
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
