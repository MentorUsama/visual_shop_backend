from django.db import models
from django.contrib.auth.models import User
from django.core.validators import  RegexValidator
from customer.models.City import City
from django.db.models.signals import pre_save

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(blank=True, max_length=100)
    address = models.CharField(blank=True, max_length=100)
    contact = models.CharField(blank=True, max_length=11, validators=[RegexValidator("^[0-9]{11}$", 'Contact number should consist of 11 digits')])
    jazzCashNumber = models.CharField(blank=True, max_length=11, validators=[RegexValidator("^[0-9]{11}$", 'Contact number should consist of 11 digits')])
    cardNumber = models.CharField(blank=True, max_length=30)
    cardExpiryDate = models.DateField(null=True, blank=True)
    CVC = models.IntegerField(null=True, blank=True)
    cityId = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='City')
    authType=models.CharField(max_length=20,default="email",choices=(("email","EMAIL"),("google","GOOGLE")))
    def __str__(self):
        return ""+self.name
def username_check(sender, instance, **kwargs):
    instance.username=instance.username.lower()
    instance.email=instance.email.lower()
pre_save.connect(username_check, sender=User)
