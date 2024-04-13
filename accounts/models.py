from django.db import models

from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=254 , unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100 , blank=True , null = True)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    is_seller = models.BooleanField(null = True , blank=True,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    

    
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.IntegerField(unique=True, null = True, blank=True)
    gender = models.CharField(max_length=10, null = True, blank=True)
    address = models.TextField( null = True, blank=True)
    

class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True,null=True)
    phone = models.IntegerField(unique=True, blank=True,null=True)
    gender = models.CharField(max_length=10, null = True, blank=True)
    alt_phone = models.IntegerField(unique=True, blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    shop_name = models.CharField(max_length=250)
    pan_number = models.CharField(max_length=11, blank=True,null=True)
    gst_number = models.CharField(max_length=50, blank=True,null=True)
    def __str__(self):
        return self.user.email
    
class address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()