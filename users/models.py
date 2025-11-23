from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Модель пользователей"""

    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users_avatars/', verbose_name='Аватар', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name='Страна')
    is_active = models.BooleanField(default=False, verbose_name='Активирован')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['email']
        permissions = [('can_disable_user', 'can disable user'), ]
