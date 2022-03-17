from django.db import models
from shop.models.Product import Product
from shop.models.Images import Images

class Features(models.Model):
    feature=models.CharField(max_length=60,null=False,blank=False)
    percentage=models.FloatField(default=0)
    productId=models.ForeignKey(Product,on_delete=models.CASCADE,null=False,blank=False,verbose_name='Product')
    imageId=models.ForeignKey(Images,on_delete=models.CASCADE,null=False,blank=False,verbose_name='Image')
