from django.db.models import fields
from rest_framework import serializers
from .models import Product,Images,Feedback
from customer.models import Customer



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
class SubcategorySerializer(serializers.ModelSerializer):
    categoryId=CategorySerializer
    class Meta:
        fields="__all__"
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Images
        fields=['id','imageColor','image']
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['id','name']
class FeedbackSerializer(serializers.ModelSerializer):
    customerId=CustomerSerializer()
    class Meta:
        model=Feedback
        depth=1
        fields=['id','rating','description','customerId']
class ProductSerializer(serializers.ModelSerializer):
    images=ImagesSerializer(many=True, read_only=True)
    feedbacks=FeedbackSerializer(many=True,read_only=True)
    subCategoryId=SubcategorySerializer
    tags=TagsSerializer
    class Meta:
        model=Product
        depth=4
        fields="__all__"