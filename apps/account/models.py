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
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=100, null=True, blank=True)

    objects = MyCustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
