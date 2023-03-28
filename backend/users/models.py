from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

ADMIN = 'admin'
REG_USER = 'user'
CHARS_FOR_EMAIL = 254
CHARS_FOR_PASSWORD = 150
CHARS_FOR_ROLE = 5
CHARS_FOR_USERNAME = 150
CHARS_FOR_FIRST_NAME = 150
CHARS_FOR_LAST_NAME = 150


class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('role', ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (REG_USER, 'User')
    )
    role = models.CharField(choices=USER_TYPE_CHOICES,
                            max_length=CHARS_FOR_ROLE,
                            default=REG_USER,
                            verbose_name='статус')
    email = models.EmailField(max_length=CHARS_FOR_EMAIL,
                              blank=False,
                              null=False,
                              unique=True,
                              verbose_name='Е-мейл')
    password = models.CharField(max_length=CHARS_FOR_PASSWORD,
                                blank=True,
                                null=True,
                                verbose_name='Пароль')
    # id =
    username = models.CharField(max_length=CHARS_FOR_USERNAME,
                                blank=False,
                                null=False,
                                unique=True,
                                verbose_name='Логин')
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
