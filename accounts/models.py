from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
import uuid

class CustomUser(AbstractUser):
    '''This is a customuser model since we need uuid for the id, and it also takes email id instead of username'''
    uuid = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    '''This defines the user model, which has the username'''
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)