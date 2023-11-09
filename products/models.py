from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    descreption = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rateings = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True,on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, null=True,on_delete=models.SET_NULL)
    comment = models.TextField(max_length=1000)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment