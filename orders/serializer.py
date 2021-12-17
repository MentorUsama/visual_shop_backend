from .models import Order,OrderedProduct,Cuopen
from shop.models import Product
from rest_framework import serializers

def checkAvailableQuantity(orderedProducts):
    for orderedProduct_data in orderedProducts:
        if(orderedProduct_data['productId'].quantity<=0):
            return False
    return True
def TotalPrice(orderedProducts):
    total=0
    for orderedProduct_data in orderedProducts:
        price=orderedProduct_data['totalQuantity']*orderedProduct_data['productId'].price
        total=total+price
    return total


class OrderedProductSerializer(serializers.ModelSerializer):
    totalPrice=serializers.DecimalField(decimal_places=3,max_digits=8,required=False)
    class Meta:
        model=OrderedProduct
        fields=['totalQuantity','totalPrice','colourSelected','sizeSelected','productId']

class OrderSerializer(serializers.ModelSerializer):
    orderedProducts=OrderedProductSerializer(many=True)
    totalPrice=serializers.DecimalField(decimal_places=3,max_digits=8,required=False)
    class Meta:
        model=Order
        fields=['totalPrice','shippingAddress','receiverName','receiverContact','cuopenId','customerId','cityId','orderedProducts']
    def validate_orderedProducts(self, attrs):
        if len(attrs) == 0:
            raise serializers.ValidationError('at least one offer required')
        if(checkAvailableQuantity(attrs)==False):
            raise serializers.ValidationError('One of the Product is out of stock')
        return attrs;
    def create(self, validated_data):
        # Getting the ordered Products
        ordered_products = validated_data.pop('orderedProducts')
        # Creating The Order
        orderPrices=TotalPrice(ordered_products)
        order = Order.objects.create(**validated_data,totalPrice=orderPrices)
        # Creating the orderedProduct
        for (orderedProduct_data) in (ordered_products):
            totalPrice=orderedProduct_data['productId'].price*orderedProduct_data['totalQuantity']
            OrderedProduct.objects.create(orderId=order, **orderedProduct_data,totalPrice=totalPrice)
        # Decreasing The quantity
        for (orderedProduct_data) in (ordered_products):
            product=orderedProduct_data['productId']
            product.quantity=product.quantity-1
            product.save()
        return order