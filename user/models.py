from random import choices
import string

import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save, pre_delete

import logging
logger = logging.getLogger(__name__)


def create_random_string(digits=False, num=4):
    if not digits:
        random_string = ''.join(choices(string.ascii_uppercase + string.digits, k=num))
    else:
        random_string = ''.join(choices(string.digits, k=num))
    return random_string

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, tg_id, password, **extra_fields):
        user = self.model(tg_id=tg_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, tg_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(tg_id, password, **extra_fields)

    def create_superuser(self, tg_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(tg_id, password, **extra_fields)


class SocialService(models.Model):
    name = models.CharField(max_length=120)
    icon = models.FileField(upload_to='social_service/')


    def __str__(self):
        return self.name


class User(AbstractUser):

    uuid = models.UUIDField(default=uuid.uuid4)

    tg_id = models.CharField( max_length=255, blank=False, null=True,  unique=True)
    photo_url = models.CharField( max_length=255, blank=False, null=True,  unique=True)
    firstname = models.CharField( max_length=255, blank=False, null=True,  unique=True)
    lastname = models.CharField( max_length=255, blank=False, null=True,  unique=True)
    username = models.CharField( max_length=255, blank=False, null=True,  unique=True)
    balance = models.IntegerField(default=0)
    rating = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    is_verified = models.BooleanField(default=False, null=False)

    USERNAME_FIELD = 'tg_id'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'{self.tg_id}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = '1. Пользователи'


class UserService(models.Model):
    service = models.ForeignKey(SocialService, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social')
    link = models.CharField(max_length=255, blank=False, null=True, unique=True)