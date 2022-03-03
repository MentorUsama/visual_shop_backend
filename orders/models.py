from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from customer.models import Customer, City
from shop.models import Product

# Create your models here.


class Cuopen(models.Model):
    minPurchase = models.DecimalField(
        decimal_places=3,verbose_name='Minimum Purcase', max_digits=8, validators=[MinValueValidator(0)])
    expiryDate = models.DateField(verbose_name='Expiry Date')
    totalQuantity = models.IntegerField(verbose_name='Total Quantity',validators=[MinValueValidator(0)])
    discountPercentage = models.IntegerField(
        default=0,verbose_name='Discount', validators=[MinValueValidator(0)])
    cuopenCode = models.IntegerField(unique=True,verbose_name='Cuopen')

    def __str__(self):
        return f'{self.cuopenCode}: for purchase > {self.minPurchase} till: {self.expiryDate}'
    class Meta:
        verbose_name_plural = "Cuopens"


class Order(models.Model):
    orderDate = models.DateField(auto_now_add=True,verbose_name='Date')
    totalPrice = models.DecimalField(decimal_places=3, max_digits=8,verbose_name='Total Price')
    shippingAddress = models.TextField(verbose_name='Address')
    receiverName = models.CharField(max_length=50,verbose_name='Name')
    receiverContact = models.CharField(max_length=11,verbose_name='Contact', validators=[RegexValidator(
        "^[0-9]{11}$", 'Contact number should consist of 11 digits')])
    orderStatus = models.CharField(max_length=50, verbose_name='Status',default="PAYMENTPENDING", choices=(
        ("shipping", "SHIPPING"), 
        ("received", "RECEIVED"), 
        ("Payment pending", "PAYMENTPENDING"),
        ("canceled", "CANCELED")
    ))
    cuopenId = models.ForeignKey(
        Cuopen, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cuopen')
    customerId = models.ForeignKey(Customer, on_delete=models.PROTECT,verbose_name='Customer')
    cityId = models.ForeignKey(City, on_delete=models.PROTECT,verbose_name='City')
    strip_client_id = models.CharField(max_length=500,blank=True,null=True,verbose_name='Strip id')
    stripe_client_secret=models.CharField(max_length=500,blank=True,null=True,verbose_name='Strip secret')

    def __str__(self):
        return f'{self.receiverName} : {self.orderDate}'
    class Meta:
        verbose_name_plural = "Orders"


class OrderedProduct(models.Model):
    totalQuantity = models.IntegerField(validators=[MinValueValidator(1)],verbose_name='Total Quantity')
    totalPrice = models.DecimalField(decimal_places=3, max_digits=8,verbose_name='Total Price')
    colourSelected = models.CharField(max_length=50,blank=True,null=True,verbose_name='Colour Selected')
    sizeSelected = models.CharField(max_length=50,blank=True,null=True,verbose_name='Size Selected')
    productId = models.ForeignKey(Product, on_delete=models.PROTECT,related_name="orderedProducts",verbose_name='Product')
    orderId = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orderedProducts",verbose_name='Order')

    def __str__(self):
        return f'orderId: {self.orderId}'
    class Meta:
        verbose_name_plural = "Ordered Products"

class Complaints(models.Model):
    orderId = models.OneToOneField(
        Order,verbose_name='Order', on_delete=models.CASCADE, related_name="complaints")
    complaintStatus = models.CharField(verbose_name='Complaint',max_length=50, choices=(
        ("pending", "PENDING"), ("solved", "SOLVED")), default="pending")  # should use regular expression
    class Meta:
        verbose_name_plural = "Complaints"


class Messages(models.Model):
    complainId = models.ForeignKey(
        Complaints,verbose_name='Complaint', on_delete=models.CASCADE, related_name="messages")
    message = models.TextField(max_length=1000,verbose_name='Message')
    isAdmin = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name='Date')

    class Meta:
        get_latest_by = ['date', 'id']
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.message



class Feedback(models.Model):
    rating = models.PositiveIntegerField(verbose_name='Feedback',
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(max_length=500,verbose_name='Description')
    orderedProductId = models.OneToOneField(
        OrderedProduct, on_delete=models.CASCADE,related_name="feedbacks",verbose_name='Ordered Product')

    def __str__(self):
        return str(self.rating)

    class Meta:
        verbose_name_plural = "Feedbacks"