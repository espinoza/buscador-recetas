from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=255, blank=False)
    bio = models.TextField(max_length=5000, null=True, default=None)
    birthday = models.DateField(null=True, default=None)
    level = models.SmallIntegerField(default=2)
    private_location = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(to="City", null=True,
                                 on_delete=models.SET_NULL,
                                 related_name="users")

class City(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(to="Country", on_delete=models.CASCADE,
                             default=None, related_name="cities")

class Country(models.Model):
    name = models.CharField(max_length=255)
