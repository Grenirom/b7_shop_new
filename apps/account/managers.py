from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class MyCustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Поле emails должно быть заполнено!')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_active', False)
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_staff', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)

        if kwargs.get('is_active') is not True:
            raise ValueError('Значение "is_active" у суперпользователя должно стоять "True"!')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Значение "is_superuser" у суперпользователя должно стоять "True"!')
        if kwargs.get('is_staff') is not True:
            raise ValueError('Значение "is_staff" у суперпользователя должно стоять "True"!')
        return self._create_user(email, password, **kwargs)

