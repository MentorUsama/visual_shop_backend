from typing import OrderedDict
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator
from django.db.models.signals import pre_save, post_save
from customer.models import Customer,City
from shop.models import Product
from django.dispatch import receiver
from pprint import pprint


# Create your models here.
class Cuopen(models.Model):
    minPurchase=models.DecimalField(decimal_places=3,max_digits=8,validators=[MinValueValidator(0)])
    expiryDate=models.DateField()
    totalQuantity=models.DecimalField(decimal_places=3,max_digits=8)
    cuopenCode=models.IntegerField(unique=True)
    def __str__(self):
        return f'{self.cuopenCode}: for purchase > {self.minPurchase} till: {self.expiryDate}'



class Order(models.Model):
    orderDate=models.DateField(auto_now_add=True)
    totalPrice=models.DecimalField(decimal_places=3,max_digits=8)
    shippingAddress=models.TextField()
    receiverName=models.CharField(max_length=50)
    receiverContact=models.CharField(max_length=11,validators=[RegexValidator("^[0-9]{11}$",'Contact number should consist of 11 digits')])
    orderStatus=models.CharField(max_length=50,default="pending",choices=(("pending","PENDING"),("received","RECEIVED")))
    cuopenId=models.ForeignKey(Cuopen,on_delete=models.SET_NULL,null=True,blank=True)
    customerId=models.ForeignKey(Customer,on_delete=models.PROTECT)
    cityId=models.ForeignKey(City,on_delete=models.PROTECT)
    complaintStatus=models.CharField(max_length=50,choices=(("NO","No Complain Yet"),("pending","PENDING"),("solved","SOLVED")),default="NO") # should use regular expression
    def __str__(self):
        return f'Order By: {self.receiverName}+" on "+{self.orderDate}'
# class Complaints(models.Model):
#     - orderId:str
#     - complaintStatus:str

class Messages(models.Model):
    orderId=models.ForeignKey(Order,on_delete=models.CASCADE)
    message=models.CharField(max_length=50)
    isAdmin=models.BooleanField(default=True)
    def __str__(self):
        return self.message
class OrderedProduct(models.Model):
    totalQuantity=models.IntegerField()
    totalPrice=models.DecimalField(decimal_places=3,max_digits=8)
    colourSelected=models.CharField(max_length=50)
    sizeSelected=models.CharField(max_length=50)
    productId=models.ForeignKey(Product,on_delete=models.PROTECT)
    orderId=models.ForeignKey(Order,on_delete=models.CASCADE)
    def __str__(self):
        return f'orderId: {self.orderId}'