from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.utils.upload_img import upload_img

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    #email = models.EmailField(blank=True, unique=True)
    name = models.CharField(max_length=100, blank=False)
    cpf = models.CharField(max_length=20, blank=False, unique=True)
    state = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    img = models.ImageField(upload_to=upload_img, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'cpf']

    #def __str__(self):
    #    return f"{self}"

class Pet(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    birthdate = models.DateField(blank=False, null=False)
    img1 = models.ImageField(upload_to=upload_img, height_field=None, width_field=None, max_length=None)
    img2 = models.ImageField(upload_to=upload_img, height_field=None, width_field=None, max_length=None)
    img3 = models.ImageField(upload_to=upload_img, height_field=None, width_field=None, max_length=None)
    img4 = models.ImageField(upload_to=upload_img, height_field=None, width_field=None, max_length=None)
    vacinado = models.BooleanField(default=False)
    sexo = models.CharField(max_length=1, blank=False, choices=(('m', 'MASCULINO'),('f', 'FEMININO')))
    raça = models.CharField(max_length=20, blank=False)

