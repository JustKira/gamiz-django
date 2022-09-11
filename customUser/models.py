from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.dispatch import receiver
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
    governorate = models.CharField(max_length=50, null=True)
    area = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Create your models here.


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = f" token = {reset_password_token.key}"

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
