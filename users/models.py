from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Модель пользователей"""

    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users_avatars/', verbose_name='Аватар', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
