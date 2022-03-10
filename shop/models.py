from django.db import models
from django.dispatch import receiver
import os
from shop.models.Category import Category
from shop.models.Images import Images
from shop.models.Product import Product
from shop.models.SubCategory import SubCategory
from shop.models.Tags import Tags

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
            