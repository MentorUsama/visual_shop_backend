from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator 
from shop.models.Tags import Tags
from shop.models.SubCategory import SubCategory
import re

class Product(models.Model):
    name=models.CharField(max_length=200)
    quantity=models.IntegerField(validators=[MinValueValidator(0)])
    price=models.DecimalField(decimal_places=3,max_digits=8,validators=[MinValueValidator(1)])
    description=models.TextField(max_length=800)
    sizes=models.CharField(max_length=50,blank=True,null=True,validators=[RegexValidator(regex="^([a-z0-9\s]+,)*([a-z0-9\s]+){1}$",message="The sizes must be comma seperated",flags=re.I)])
    tags=models.ManyToManyField(Tags)
    subCategoryId=models.ForeignKey(SubCategory,on_delete=models.PROTECT,verbose_name='Subcategory')


    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        # if Video.objects.filter(field_boolean=True).exists():
        #     print('Video with field_boolean=True exists')
        # else:
        super(Product, self).save(*args, **kwargs)
    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Products"
        