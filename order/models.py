from django.db import models
from operator import mod
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERD = 'Deliverd'

class PaymentStatus(models.TextChoices):
    PAID = 'Paid'
    UNPAID = 'unpaid'

class PaymentMod(models.TextChoices):
    COD = 'COD' # Cash On deliver
    CARD = 'CARD'

class Order(models.Model):
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=11)
    total_amount = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_Mod = models.CharField(max_length=10, choices=PaymentMod.choices, default=PaymentMod.COD)
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    user = models.ForeignKey(User, null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True,on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True,on_delete=models.CASCADE, related_name='orderitems')
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name