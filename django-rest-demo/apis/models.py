from asyncio.windows_events import NULL
from pyexpat import model
import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
import datetime


from .managers import CustomUserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'user'

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=30)
    modified_by = models.CharField(max_length=30)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
        
class TableA(models.Model):
    class Meta:
        db_table = 'table_a'
    field1 = models.IntegerField()

class TableB(models.Model):
    class Meta:
        db_table = 'table_b'
    id_a = models.ForeignKey(TableA,on_delete=models.CASCADE)
    field1 = models.IntegerField()
    field2 = models.IntegerField()

class TableC(models.Model):
    class Meta:
        db_table = 'table_c'
    id_a = models.ForeignKey(TableA,on_delete=models.CASCADE)
    field1 = models.IntegerField()
    field2 = models.IntegerField()
    