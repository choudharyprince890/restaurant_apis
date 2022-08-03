from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
import uuid
from.manager import AccountManager
from datetime import date, datetime
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    RESTAURANT = 2 

    ROLE = (
        (ADMIN, 'admin'),
        (RESTAURANT, 'restaurant')
    )
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public Id')
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, default='2', choices=ROLE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    @property
    def is_staff(self):
        return self.is_active

    objects = AccountManager()




class Restaurant_owner(models.Model):
    Delete_STATUS = (
    ('Active', 'Active'),
    ('InActive', 'InActive')
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=80)
    shop = models.CharField(max_length=80)
    dish = models.CharField(max_length=50)
    menu = models.CharField(max_length=80)
    status  = models.CharField(max_length=100, default='Active', choices=Delete_STATUS)
    created_on = models.DateTimeField(default=datetime.now)