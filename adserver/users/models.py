from django.db import models
from django.contrib.auth.models import User
from .validators import PhoneValidator

from rest_framework import validators


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, unique=True, validators=[PhoneValidator, ])

    profile_pic = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'