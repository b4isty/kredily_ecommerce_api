from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUserModel(AbstractUser):
    """
    Custom user model
    to open the scope of email authentication
    """
    pass
