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
    avatar = models.TextField(default='https://res.cloudinary.com/dpmhx7k6y/image/upload/v1684286943/PleaseHelp/UserProfiles/g5kzvqkmlmqtomuamdzp.png', null=True, blank=True)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default='Client', max_length=20)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5)
    feedback_count = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=25, blank=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)

    
    def __str__(self):
        return self.username
    
    def is_client(self):
        return self.user_type == 'Client'
    
    def is_vendor(self):
        return self.user_type == 'Vendor'

    def add_rating(self, new_rating):
        total_before_new_rating = self.rating * self.feedback_count
        self.feedback_count += 1
        total_after_new_rating = total_before_new_rating + new_rating
        self.rating = total_after_new_rating / self.feedback_count
        self.save()

        
    class Meta:
        ordering = ['first_name', 'last_name']
    
    REQUIRED_FIELDS = ['email', 'password']
    USERNAME_FIELD = 'username'