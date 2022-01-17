from operator import mod
from statistics import mode
from django.db.models import fields
from django.forms import IntegerField, models
from rest_framework import serializers
from .models import Category, Product,Images,Feedback, Tags,SubCategory
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



class GetAllTagSerializer(serializers.ModelSerializer):
    nused=serializers.IntegerField()
    class Meta:
        model=Tags
        fields=['nused','id','name']
        extra_kwargs = {
            'nused': {'read_only': True}
        }



class GetAllSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategory
        fields="__all__"
class GetAllCategoriesSerializer(serializers.ModelSerializer):
    Subcategories=GetAllSubcategorySerializer(many=True,read_only=True)
    class Meta:
        model=Category
        depth=2
        fields=['id','name','Subcategories']