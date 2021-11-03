from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=30,null=True)
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=100,null=False)
    address=models.CharField(max_length=100,null=True)
    contact=models.CharField(max_length=11,null=True)