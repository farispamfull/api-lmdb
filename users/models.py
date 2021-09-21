from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    first_name = models.CharField(
        max_length=50, blank=True, verbose_name='First name')
    last_name = models.CharField(
        max_length=50, blank=True, verbose_name='Last name')
    username = models.CharField(max_length=50, unique=True)
    bio = models.TextField(blank=True, verbose_name='Description')
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(max_length=10, blank=True,
                            choices=UserRoles.choices, default=UserRoles.USER)

    REQUIRED_FIELDS = ('email',)

    @property
    def is_admin(self):
        return (self.role == UserRoles.ADMIN
                or self.is_staff or self.is_superuser)

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['username']
