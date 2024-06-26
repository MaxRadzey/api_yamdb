from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from users.constants import (USER, ROLE_CHOICES, ADMIN,
                             MODERATOR, ROLE_MAX_LENGTH)


class DBUserManager(BaseUserManager):

    def create_user(
            self,
            username,
            email=None,
            password=None,
            **extra_fields
    ):
        if not username:
            raise ValueError('Поле username обязательное для заполнения')
        if username.lower() == 'me':
            raise ValueError('Имя пользователя не может быть "me"')
        if not email:
            raise ValueError('Поле email обязательное для заполнения')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            username,
            email=None,
            password=None,
            **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)


class DBUser(AbstractUser):

    objects = DBUserManager()
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
    )

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR
