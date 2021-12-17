from django.db.models import fields
from .models import Order,OrderedProduct,Cuopen
from rest_framework import serializers


class OrderedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderedProduct
        fields="__all__"
class OrderSerializer(serializers.ModelSerializer):
    orderedProducts=OrderedProductSerializer(many=True)
    class Meta:
        model=Order
        exclude=['orderStatus','orderDate']
    def validate_orderedProducts(self, attrs):
        if len(attrs) == 0:
            raise serializers.ValidationError('at least one offer required')
        return attrs