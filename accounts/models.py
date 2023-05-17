from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Client', 'Client'),
        ('Vendor', 'Vendor'),
        ('Support', 'Support'),
        ('Manager', 'Manager')
    )
    
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to='static/images/avatars', default='static/images/avatars/default_avatar.png')
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default='Client', max_length=20)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=25, blank=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)

    
    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['first_name', 'last_name']
    
    REQUIRED_FIELDS = ['email', 'password']
    USERNAME_FIELD = 'username'
