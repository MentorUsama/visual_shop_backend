from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator 
from customer.models import Customer
from django.dispatch import receiver
import re
import os

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    name=models.CharField(max_length=20)
    categoryId=models.ForeignKey(Category,on_delete=models.PROTECT)
    class Meta:
        ordering = ['categoryId'] #Sort in desc order
    def __str__(self):
        return f'{self.categoryId} > {self.name}'
class Tags(models.Model):
    name=models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Tags, self).save(*args, **kwargs)




class Product(models.Model):
    name=models.CharField(max_length=200)
    quantity=models.IntegerField(validators=[MinValueValidator(0)])
    price=models.DecimalField(decimal_places=3,max_digits=8,validators=[MinValueValidator(1)])
    description=models.TextField(max_length=800)
    sizes=models.CharField(max_length=50,default="None",validators=[RegexValidator(regex="^([a-z0-9\s]+,)*([a-z0-9\s]+){1}$",message="The sizes must be comma seperated",flags=re.I)])
    tags=models.ManyToManyField(Tags)
    subCategoryId=models.ForeignKey(SubCategory,on_delete=models.PROTECT)


    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        # if Video.objects.filter(field_boolean=True).exists():
        #     print('Video with field_boolean=True exists')
        # else:
        super(Product, self).save(*args, **kwargs)
    class Meta:
        ordering = ['-id']





class Feedback(models.Model):
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description=models.TextField(max_length=500)
    customerId=models.ForeignKey(Customer,on_delete=models.CASCADE)
    productId=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="feedbacks")
    def __str__(self):
        return str(self.rating)

class Images(models.Model):
    image=models.ImageField()
    productId=models.ForeignKey(Product,on_delete=models.CASCADE,null=False,blank=False,related_name='images')
    imageColor=models.CharField(max_length=20,blank=True,null=True)










# ==================== Signals for Image deleted or updated =============
@receiver(models.signals.post_delete, sender=Images)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
@receiver(models.signals.pre_save, sender=Images)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = Images.objects.get(pk=instance.pk).image
    except object.DoesNotExist:
        return False
    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)