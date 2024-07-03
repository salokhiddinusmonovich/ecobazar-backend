from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    profile_image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    realname = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']





    def __str__(self):
        return self.email

