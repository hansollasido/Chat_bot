from asyncore import write
from operator import mod
from time import timezone
from turtle import title
from unicodedata import name
from django.db import models
from datetime import datetime



# Create your models here.
class Board(models.Model):
    author = models.CharField(max_length=10, null=False)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class data_save(models.Model):
    d_q = models.CharField(max_length= 1000)
    d_a = models.CharField(max_length= 1000)
    def __str__(self):
        return self.d_q+self.d_a
