from operator import mod
from statistics import mode
from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=250, blank=False)
    content = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #Foreign Keys
    Post_Id = models.ForeignKey('Post', on_delete=models.CASCADE)