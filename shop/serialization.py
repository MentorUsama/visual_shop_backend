from django.db.models import fields
from rest_framework import serializers
from .models import Product,Images



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
        fields="__all__"
class ProductSerializer(serializers.ModelSerializer):
    images=ImagesSerializer(many=True, read_only=True)
    subCategoryId=SubcategorySerializer
    tags=TagsSerializer
    class Meta:
        model=Product
        depth=3
        fields="__all__"