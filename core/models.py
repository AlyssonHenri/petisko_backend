from django.db import models

from django.contrib.auth.models import AbstractUser
from core.utils.upload_img import upload_img

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=100, blank=False)
    cpf = models.CharField(max_length=11, blank=False)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    img = models.ImageField(upload_to=upload_img)

    #def __str__(self):
    #    return f"{self}"