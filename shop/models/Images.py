from shop.models.Product import Product
from django.db import models

class Images(models.Model):
    image=models.ImageField()
    productId=models.ForeignKey(Product,on_delete=models.CASCADE,null=False,blank=False,related_name='images',verbose_name='Product')
    imageColor=models.CharField(max_length=20,blank=True,null=True,verbose_name='Color')
