from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    
    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_auth'
            )
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'