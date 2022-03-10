from django.db import models
from orders.models.Cuopen import Cuopen
from customer.models.Customer import Customer
from customer.models.City import City
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from orders.models.stripe import Stripe


class Order(models.Model):
    orderDate = models.DateField(auto_now_add=True,verbose_name='Date')
    totalPrice = models.DecimalField(decimal_places=3, max_digits=8,verbose_name='Total Price')
    shippingAddress = models.TextField(verbose_name='Address')
    receiverName = models.CharField(max_length=50,verbose_name='Name')
    receiverContact = models.CharField(max_length=11,verbose_name='Contact', validators=[RegexValidator(
        "^[0-9]{11}$", 'Contact number should consist of 11 digits')])
    orderStatus = models.CharField(max_length=20, verbose_name='Status', choices=(
        ("shipping", "SHIPPING"), 
        ("received", "RECEIVED"), 
        ("packaging", "PACKAGING"),
        ("Payment_pending", "PAYMENTPENDING"),
        ("canceled", "CANCELED")
    ))
    paymentMethod = models.CharField(max_length=10, verbose_name='Payment Method', choices=(
        ("CARD", "CARD"), 
        ("CASH", "CASH")
    ))
    cuopenId = models.ForeignKey(
        Cuopen, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cuopen')
    customerId = models.ForeignKey(Customer, on_delete=models.PROTECT,verbose_name='Customer')
    cityId = models.ForeignKey(City, on_delete=models.PROTECT,verbose_name='City')
    stripe = models.ForeignKey(Stripe, on_delete=models.CASCADE,verbose_name='Stripe',null=True)

    def __str__(self):
        return f'{self.receiverName} : {self.orderDate}'
    class Meta:
        verbose_name_plural = "Orders"
