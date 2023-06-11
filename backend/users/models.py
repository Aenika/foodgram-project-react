# flake8: noqa: I001, I004
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models

from core.constants import (ADMIN, CHARS_FOR_EMAIL, CHARS_FOR_FIRST_NAME,
                            CHARS_FOR_LAST_NAME, CHARS_FOR_PASSWORD,
                            CHARS_FOR_ROLE, CHARS_FOR_USERNAME, REG_USER)

class CustomUserManager(UserManager):
    """Класс для создания суперпользователя."""
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('role', ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """Класс для представления пользователей."""
    USER_TYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (REG_USER, 'User')
    )
    role = models.CharField(choices=USER_TYPE_CHOICES,
                            max_length=CHARS_FOR_ROLE,
                            default=REG_USER,
                            verbose_name='Статус')
    email = models.EmailField(max_length=CHARS_FOR_EMAIL,
                              blank=False,
                              null=False,
                              unique=True,
                              verbose_name='Е-мейл')
    password = models.CharField(max_length=CHARS_FOR_PASSWORD,
                                blank=True,
                                null=True,
                                verbose_name='Пароль')
    username = models.CharField(max_length=CHARS_FOR_USERNAME,
                                blank=False,
                                null=False,
                                unique=True,
                                verbose_name='Логин',
                                validators=[
                                    RegexValidator(regex=r'^[\w.@+-]+\Z$')
                                ])
    first_name = models.CharField(max_length=CHARS_FOR_FIRST_NAME,
                                  blank=False,
                                  null=False,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=CHARS_FOR_LAST_NAME,
                                 blank=False,
                                 null=False,
                                 verbose_name='Фамилия')
    objects = CustomUserManager()

    @property
    def is_admin(self):
        return self.role == ADMIN

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Класс для представления подписки пользователя на другого пользователя."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь, кто подписывается',
        related_name='following'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписки',
    )

    def __str__(self):
        return f'Пользователь {self.user} подписан на автора {self.author}.'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            )
        ]
