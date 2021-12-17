from .models import Order,OrderedProduct,Cuopen
from rest_framework import serializers


class OrderedProductSerializer(serializers.ModelSerializer):
    totalPrice=serializers.DecimalField(decimal_places=3,max_digits=8,required=False)
    class Meta:
        model=OrderedProduct
        fields="__all__"
    def create(self, validated_data):
        data = validated_data.copy()
        data['totalPrice'] = 20
        return super(OrderedProductSerializer, self).create(**data)

class OrderSerializer(serializers.ModelSerializer):
    orderedProducts=OrderedProductSerializer(many=True)
    class Meta:
        model=Order
        exclude=['orderStatus','orderDate']
    def validate_orderedProducts(self, attrs):
        if len(attrs) == 0:
            raise serializers.ValidationError('at least one offer required')
        return attrs