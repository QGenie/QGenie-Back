from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager
import os


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    genders = (('female', 'Female'), ('male', 'Male'))
    def get_upload_to(self, filename):
        return os.path.join('images', 'profile_pictures', str(self.pk), filename)
    first_name = models.CharField(max_length=128, null=False, blank=False)
    last_name = models.CharField(max_length=128, null=False, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=16, choices=genders, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    picture = models.ImageField(upload_to=get_upload_to, default='images/profile_pictures/default_profile_picture.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.user.email


class VerificationCode(models.Model):
    code = models.CharField(max_length=6, null=False, blank=False)
    creationDate = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return self.user.email