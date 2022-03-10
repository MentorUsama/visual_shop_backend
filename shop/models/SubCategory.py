from django.db import models
from shop.models.Category import Category

class SubCategory(models.Model):
    name=models.CharField(max_length=20)
    categoryId=models.ForeignKey(Category,on_delete=models.PROTECT,related_name="Subcategories",verbose_name='Category')
    class Meta:
        ordering = ['categoryId'] #Sort in desc order
        verbose_name_plural = "Sub Categories"
    def __str__(self):
        return f'{self.categoryId} > {self.name}'
        