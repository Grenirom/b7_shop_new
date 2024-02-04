import uuid

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.account.managers import MyCustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Почта'
    )
    password = models.CharField(max_length=250, validators=[
        MinValueValidator(limit_value=8),
        MaxValueValidator(limit_value=20),
    ])
    is_active = models.BooleanField(default=False, verbose_name='Активен')
    is_superuser = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=500, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)

    objects = MyCustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_activation_code(self):
        code = str(uuid.uuid4())
        self.activation_code = code
        self.save()

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


