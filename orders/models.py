from django.db import models
from django.conf import settings

# Create your models here.



# start of order model
class OrderType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']


class OrderStatus(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['pk']


class OrderDifficulty(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['pk']


class Order(models.Model):
    order_name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.ForeignKey(OrderDifficulty, on_delete=models.PROTECT, related_name='order_difficulties')
    address = models.CharField(max_length=200)
    type = models.ForeignKey(OrderType, on_delete=models.PROTECT, related_name='order_types')
    location = models.CharField(max_length=200, null=True, blank=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, related_name='client_orders')
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='vendor_orders')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    special_requests = models.TextField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    status = models.ForeignKey(OrderStatus, default=1, on_delete=models.PROTECT, related_name='order_status')
    client_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    vendor_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    class Meta:
        ordering = ['-updated_date', '-created_date']

    def __str__(self):
        return self.order_name

