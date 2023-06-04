from django.contrib.auth.models import AbstractUser
from django.db import models


class UserType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "User type"
        verbose_name_plural = "User types"


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.TextField(default="https://res.cloudinary.com/dpmhx7k6y/image/upload/v1684286943/PleaseHelp/UserProfiles/g5kzvqkmlmqtomuamdzp.png", null=True, blank=True)
    user_type = models.ForeignKey(UserType, on_delete=models.PROTECT, default=10, related_name="users_type")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5)
    payment_method = models.CharField(max_length=25, blank=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.username

    def is_client(self):
        return self.user_type.pk == 10

    def is_vendor(self):
        return self.user_type.pk == 20

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    REQUIRED_FIELDS = ["email", "password"]
    USERNAME_FIELD = "username"
