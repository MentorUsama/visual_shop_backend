from .models import Order,OrderedProduct,Cuopen
from shop.models import Product
from rest_framework import serializers

def getProductsPrice(productIds):
    return Product.objects.filter(id__in=productIds).values_list('price',flat=True)
def getIds(orderedProducts):
    ids=[]
    for orderedProduct_data in orderedProducts:
        ids.append(orderedProduct_data['productId'].id)
    return ids

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
        return attrs;
    def create(self, validated_data):
        ordered_products = validated_data.pop('orderedProducts')
        ids=getIds(ordered_products)
        prices=getProductsPrice(ids)
        order = Order.objects.create(**validated_data,totalPrice=0)
        orderPrices=0;
        i=0;
        for (orderedProduct_data) in (ordered_products):
            totalPrice=prices[i]*orderedProduct_data['totalQuantity']
            orderPrices=orderPrices+totalPrice;
            OrderedProduct.objects.create(orderId=order, **orderedProduct_data,totalPrice=totalPrice)
        order.totalPrice=orderPrices
        order.save()
        return order