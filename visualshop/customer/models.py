from django.db import models
from django.core.validators import  RegexValidator
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
# Reset password libraries
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

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
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(blank=True, max_length=100)
    address = models.CharField(blank=True, max_length=100)
    contact = models.CharField(blank=True, max_length=11, validators=[RegexValidator("^[0-9]{11}$", 'Contact number should consist of 11 digits')])
    jazzCashNumber = models.CharField(blank=True, max_length=11, validators=[RegexValidator("^[0-9]{11}$", 'Contact number should consist of 11 digits')])
    cardNumber = models.CharField(blank=True, max_length=30)
    cardExpiryDate = models.DateField(null=True, blank=True)
    CVC = models.IntegerField(null=True, blank=True)
    cityId = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    authType=models.CharField(max_length=20,default="email",choices=(("email","EMAIL"),("google","GOOGLE")))
    def __str__(self):
        return ""+self.name


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@visualshop.local",
        # to:
        [reset_password_token.user.email]
    )