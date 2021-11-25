from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator
from customer.models import Customer,City
from shop.models import Product


# Create your models here.
class Cuopen(models.Model):
    minPurchase=models.DecimalField(decimal_places=3,max_digits=8,validators=[MinValueValidator(0)])
    expiryDate=models.DateField()
    totalQuantity=models.DecimalField(decimal_places=3,max_digits=8)
    cuopenCode=models.IntegerField()
    def __str__(self):
        return self.cuopenCode

class Order(models.Model):
    orderDate=models.DateField(auto_now_add=True)
    totalPrice=models.DecimalField(decimal_places=3,max_digits=8)
    shippingAddress=models.TextField()
    receiverName=models.CharField(max_length=50)
    receiverContact=models.CharField(max_length=11,validators=[RegexValidator("^[0-9]{11}$",'Contact number should consist of 11 digits')])
    orderStatus=models.CharField(max_length=50, validators=[RegexValidator('^pending$|^received$','Order Status can only be pending,received')])
    cuopenId=models.ForeignKey(Cuopen,on_delete=models.SET_NULL,null=True,blank=True)
    customerId=models.ForeignKey(Customer,on_delete=models.PROTECT)
    cityId=models.ForeignKey(City,on_delete=models.PROTECT)
    complaintStatus=models.CharField(max_length=50,validators=[RegexValidator('^null$|^solved$|^pending$','Order Status can only be null,pending,solved')]) # should use regular expression
    def __str__(self):
        return self.receiverName+" on "+self.receiverContact
        
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
        return self.orderId