import imp
from operator import mod
from pyexpat import model
from statistics import mode
from tkinter.tix import Tree
from django.db.models import fields
from django.forms import IntegerField, models
from rest_framework import serializers

from .models import Category, Product, Images, Tags, SubCategory
from orders.models import OrderedProduct,Feedback
from customer.models import Customer


# ========== Gettting All The Product With As Much Data Possible ==========
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
class SubcategorySerializer(serializers.ModelSerializer):
    categoryId = CategorySerializer

    class Meta:
        fields = "__all__"
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'imageColor', 'image']
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
class OrderedProductSerializer(serializers.ModelSerializer):
    feedbacks=FeedbackSerializer(many=True, read_only=True)
    class Meta:
        model = OrderedProduct
        fields = ['feedbacks']
class ProductSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    orderedProducts = OrderedProductSerializer(many=True, read_only=Tree)
    subCategoryId = SubcategorySerializer
    tags = TagsSerializer
    class Meta:
        model = Product
        depth = 4
        fields = "__all__"


# =========== Getting All Tags ===========
class GetAllTagSerializer(serializers.ModelSerializer):
    nused = serializers.IntegerField()
    class Meta:
        model = Tags
        fields = ['nused', 'id', 'name']
        extra_kwargs = {
            'nused': {'read_only': True}
        }


# =========== Getting All Subcategory ===========
class GetAllSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


# =========== Getting All Category Serizlizer ===========
class GetAllCategoriesSerializer(serializers.ModelSerializer):
    Subcategories = GetAllSubcategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        depth = 2
        fields = ['id', 'name', 'Subcategories']
