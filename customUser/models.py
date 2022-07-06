from datetime import datetime
from pyexpat import model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.forms import CharField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .cUserManager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=50, unique=False)
    lastname = models.CharField(max_length=50, unique=False)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=50, unique=True)
    birthday = models.DateField(null=True)
    phone = models.IntegerField(null=True)
    location = models.CharField(max_length=50, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
# Create your models here.
