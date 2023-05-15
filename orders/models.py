from django.db import models
from accounts.models import User

# Create your models here.


# start of order model
class Order(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Moderate', 'Moderate'),
        ('Hard', 'Hard'),
    ]
    TYPE_CHOICES = [
        ('Office', 'Office'),
        ('Home', 'Home'),
        ('Carpet', 'Carpet'),
        ('Window', 'Window'),
        ('Bathroom', 'Bathroom'),
    ]
    STATUS_CHOICES = [
        ('Posted', 'Posted'), #posted, requested, pending (which one?)
        ('Accepted', 'Accepted'),
        ('Verified', 'Verified'),
        ('In_progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    order_name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    address = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=200)
    client = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='client_orders')
    vendor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='vendor_orders')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    special_requests = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Posted')
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    class Meta:
        ordering = ['-updated_date', '-created_date']

    def __str__(self):
        return self.order_name
