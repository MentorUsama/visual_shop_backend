from shop.models.Product import Product
from visualshop.settings import STATIC_ROOT
from visualshop.settings import BASE_DIR
from django.db import models
from django.dispatch import receiver
import os
from shop.models.Images import Images
from visualshop.utility.model_utility import *
from visualshop.utility.model_config import *
# from shop.models.Features import Features
from shop.core.utility.get_model_result import get_model_result
# from shop.core.features.write import bulk_create
# ==================== Signals for Image deleted or updated =============
@receiver(models.signals.post_delete, sender=Images)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    # File is deleted so also deleting the image
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)
    # Deleting the features related to that image
    # Features.objects.filter(imageId=instance.id).delete()

@receiver(models.signals.pre_save, sender=Images)
def auto_delete_file_on_change(sender, instance, **kwargs):
    # Checking if file is going to be added first time
    if not instance.pk:
        return False
    # Getting the old image
    try:
        old_file = Images.objects.get(pk=instance.pk).image
    except object.DoesNotExist:
        return False
    # Deleting the old image
    new_file = instance.image
    if not old_file == new_file:
        if os.path.exists(old_file.path):
            os.remove(old_file.path)

@receiver(models.signals.post_save, sender=Images)
def image_on_save(sender, instance, **kwargs):
    # Loading files
    deep_feats_loaded, color_feats_loaded, labels_loaded = load_feat_db_different_file("all_feat.npy","all_feat.list","all_color_feat.npy")
    
    # Getting related data
    image_url = os.path.join(BASE_DIR,"static","images",instance.image.name)
    product_id = instance.productId
    image_id=instance.id
    label=instance.image.name+" "+str(product_id)+" "+str(image_id)+"\n"

    # getting new deep and color feature
    extractor = load_test_model()
    single_deep_feat, single_color_feat = dump_single_feature(image_url, extractor)
    save_new_feature(deep_feats_loaded,color_feats_loaded,labels_loaded,single_deep_feat,single_color_feat,label)
    return
    