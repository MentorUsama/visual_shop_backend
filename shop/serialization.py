from pyexpat import model
from django.db.models import fields
from django.forms import IntegerField, models
from rest_framework import serializers

from shop.models.Category import Category
from shop.models.Product import Product
from shop.models.Images import Images
from shop.models.Tags import Tags
from shop.models.SubCategory import SubCategory

from orders.models.OrderedProduct import OrderedProduct
from orders.models.Feedback import Feedback
from orders.models.Order import Order
from customer.models.Customer import Customer
# from shop.models.Features import Features


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
        fields = ['rating','description','id']
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['name','id']
class OrderSerializer(serializers.ModelSerializer):
    customerId=CustomerSerializer()
    class Meta:
        model=Order
        fields=['customerId']
class OrderedProductSerializer(serializers.ModelSerializer):
    feedback=FeedbackSerializer(many=False, read_only=True,source="feedbacks")
    customer=OrderSerializer(source="orderId")
    class Meta:
        model = OrderedProduct
        fields = ['feedback','customer']
class ProductSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    feedbacks = OrderedProductSerializer(many=True, read_only=True,source="orderedProducts")
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


# Feature Serialize
# class FeatureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Features
#         fields="__all__"