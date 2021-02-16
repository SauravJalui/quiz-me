from django.contrib.auth.models import AbstractUser
from django.db import models

# using CustonUser model for scalability
class CustomUser(AbstractUser):
    pass
