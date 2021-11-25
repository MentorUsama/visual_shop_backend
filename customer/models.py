from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.base import Model
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models.fields.related import ForeignKey

# Create your models here.


class Province(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=20)
    provinceId = ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Customer(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(blank=True, max_length=100)
    password = models.CharField(max_length=32)
    address = models.CharField(blank=True, max_length=100)
    contact = models.CharField(blank=True, max_length=11, validators=[RegexValidator("^[0-9]{11}$", 'Contact number should consist of 11 digits')])
    jazzCashNumber = models.CharField(blank=True, max_length=11, validators=[RegexValidator("^[0-9]{11}$", 'Contact number should consist of 11 digits')])
    cardNumber = models.CharField(blank=True, max_length=30)
    cardExpiryDate = models.DateField(null=True, blank=True)
    CVC = models.IntegerField(null=True, blank=True)
    cityId = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.email
