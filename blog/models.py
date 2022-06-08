from operator import mod
from django.db import models

import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True,unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=False, max_length=150)
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return self.email



class Post(models.Model):
    id = models.UUIDField(primary_key=True,unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, blank=False)
    content = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #Foreign Keys
    User_Id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True,unique=True, default=uuid.uuid4, editable=False)
    content = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #Foreign Keys
    User_Id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    Post_Id = models.ForeignKey('Post', on_delete=models.CASCADE)