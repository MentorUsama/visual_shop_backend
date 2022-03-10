from shop.models.Product import Product
from django.db import models
from django.dispatch import receiver
import os

class Images(models.Model):
    image=models.ImageField()
    productId=models.ForeignKey(Product,on_delete=models.CASCADE,null=False,blank=False,related_name='images',verbose_name='Product')
    imageColor=models.CharField(max_length=20,blank=True,null=True,verbose_name='Color')


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
            