from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField

class User(AbstractUser):
    def __str__(self):
        return self.username
    closed = models.CharField(max_length=100, default="")
    tos_violation = models.CharField(max_length=100, default="")
    title = models.CharField(max_length=100, default="")