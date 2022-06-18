from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True)
    email = models.EmailField(verbose_name='e-mail', unique=True)
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    
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
        
        
class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='follows_unique'
            )
        ]