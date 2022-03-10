from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from orders.models.Order import Order
from shop.models.Product import Product

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
        