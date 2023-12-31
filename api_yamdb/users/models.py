from django.contrib.auth.models import AbstractUser
from django.db import models


class DBUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    ]

    password = models.CharField(max_length=128, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)
    confirmation_code = models.CharField(max_length=6, blank=True)
