from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

#---------------------------------------------------------------------------------------#

class ForgetPassword(models.Model):
    email = models.EmailField(max_length=255)
    token = models.CharField(max_length=255, unique=True)


