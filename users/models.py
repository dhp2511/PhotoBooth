from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import UserManager

class User(AbstractUser):
    user_bio = models.CharField(max_length=500 ,default='',null=True, blank=True)
    pfp = models.ImageField(default=None , null=True, blank=True,upload_to='pfp/')
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    
    objects = UserManager()
    
    
