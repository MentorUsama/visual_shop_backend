from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from customer.models import Customer

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name
class SubCategory(models.Model):
    name=models.CharField(max_length=20)
    categoryId=models.ForeignKey(Category,on_delete=models.PROTECT)
    def __str__(self):
        return self.name
class Tags(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name





class Product(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField(max_length=300)
    # - attributes---pending
    tags=models.ManyToManyField(Tags)
    subCategoryId=models.ForeignKey(SubCategory,on_delete=models.PROTECT)
    def __str__(self):
        return self.name





class Feedback(models.Model):
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description=models.TextField(max_length=200)
    customerId=models.ForeignKey(Customer,on_delete=models.CASCADE)
    productId=models.ForeignKey(Product,on_delete=models.CASCADE)
    def __str__(self):
        return self.rating

class Images(models.Model):
    url=models.TextField(max_length=150)
    productId=models.ForeignKey(Product,on_delete=models.CASCADE)
    imageColor=models.CharField(max_length=20,blank=True,null=True)