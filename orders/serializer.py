from django.db.models import fields
from .models import Order,OrderedProduct,Cuopen
from rest_framework import serializers


class OrderedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderedProduct
        fields="__all__"
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        exclude=['orderStatus','orderDate']
        extra_kwargs = {
            'totalPrice': {'read_only': True},
            'customerId':{'read_only':True}
        }