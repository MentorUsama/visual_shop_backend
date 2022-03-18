from shop.models.Product import Product
from django.db import models
from django.dispatch import receiver
import os
from shop.models.Images import Images
from shop.models.Features import Features
from shop.core.utility.get_model_result import get_model_result
from shop.core.features.write import bulk_create
# ==================== Signals for Image deleted or updated =============
@receiver(models.signals.post_delete, sender=Images)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    pass
    # print("------------------------------ on delete ---------------------")
    # # File is deleted so also deleting the image
    # if instance.image:
    #     if os.path.exists(instance.image.path):
    #         os.remove(instance.image.path)
    # # Deleting the features related to that image
    # Features.objects.filter(imageId=instance.id).delete()

@receiver(models.signals.pre_save, sender=Images)
def auto_delete_file_on_change(sender, instance, **kwargs):
    pass
    # # Checking if file is going to be added first time
    # if not instance.pk:
    #     return False
    # # Getting the old image
    # try:
    #     old_file = Images.objects.get(pk=instance.pk).image
    # except object.DoesNotExist:
    #     return False
    # # Deleting the old image
    # new_file = instance.image
    # if not old_file == new_file:
    #     if os.path.exists(old_file.path):
    #         os.remove(old_file.path)

@receiver(models.signals.post_save, sender=Images)
def image_on_save(sender, instance, **kwargs):
    pass
    # print("on_save")
    # # If features already exist for that image then deleting it
    # try:
    #     feature_prev=Features.objects.filter(imageId=instance.id)
    #     feature_prev.delete()
    # except Features.DoesNotExist:
    #     feature_prev=None
    # # Adding the feature of image
    # all_features=get_model_result(instance.image)
    
    # if(len(all_features)!=0):
    #     bulk_create(all_features,instance,instance.productId)