from .models import Order,OrderedProduct
from datetime import date
from rest_framework import serializers





# ============= Utitlity Function for Orders =============
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
# ============= Serializer For Creating the order =============
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
        fields=['totalPrice','shippingAddress','receiverName','receiverContact','cuopenId','customerId','cityId','orderedProducts','orderStatus']
        extra_kwargs = {'orderStatus': {'read_only': True}, }
    def validate_orderedProducts(self, attrs):
        if len(attrs) == 0:
            raise serializers.ValidationError('At least One Product is Required')
        if(checkAvailableQuantity(attrs)==False):
            raise serializers.ValidationError('One of the Product is out of stock')
        return attrs;
    def validate_cuopenId(self, attrs):
        if(attrs!=None):
            today = date.today()
            if(attrs.expiryDate<today):
                raise serializers.ValidationError('Ooops Token has expired!!')
            if(attrs.totalQuantity<=0):
                raise serializers.ValidationError('Token Limit Reached!!')  
        return attrs
    def create(self, validated_data):
        # Getting the ordered Products
        ordered_products = validated_data.pop('orderedProducts')
        # Calculating the Total Price
        orderPrices=TotalPrice(ordered_products)
        if(validated_data['cuopenId']!=None):
            if(orderPrices<validated_data['cuopenId'].minPurchase):
                raise serializers.ValidationError({"cuopenId":["Total Purchase must be greater then "+str(validated_data['cuopenId'].minPurchase)+""]})
            discout=(validated_data['cuopenId'].discountPercentage*orderPrices)/100
            orderPrices=orderPrices-discout
            validated_data['cuopenId'].totalQuantity=validated_data['cuopenId'].totalQuantity-1
            validated_data['cuopenId'].save()
        # Creating The order
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
# ============= Serializer For checking Cuopen =============
class CheckOrderedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderedProduct
        fields=['totalQuantity','productId']
class CheckOrderSerializer(serializers.ModelSerializer):
    orderedProducts=CheckOrderedProductSerializer(many=True)
    totalPrice=serializers.DecimalField(decimal_places=3,max_digits=8,required=False)
    class Meta:
        model=Order
        fields=['totalPrice','cuopenId','orderedProducts']
    def validate_orderedProducts(self, attrs):
        if len(attrs) == 0:
            raise serializers.ValidationError('At least One Product is Required')
        return attrs;
    def validate_cuopenId(self, attrs):
        today = date.today()
        if(attrs.expiryDate<today):
            raise serializers.ValidationError('Ooops Token has expired!!')
        if(attrs.totalQuantity<=0):
            raise serializers.ValidationError('Token Limit Reached!!')  
        return attrs
    def save(self):
        # Getting the ordered Products
        ordered_products = self.validated_data['orderedProducts']
        # Calculating the Total Price
        orderPrices=TotalPrice(ordered_products)
        if(orderPrices<self.validated_data['cuopenId'].minPurchase):
            raise serializers.ValidationError({"cuopenId":["Total Purchase must be greater then "+str(self.validated_data['cuopenId'].minPurchase)+""]})
        discout=(self.validated_data['cuopenId'].discountPercentage*orderPrices)/100
        discout=orderPrices-discout
        return {"totalPrice":orderPrices,"discountPrice":discout,'cuopenId':self.validated_data['cuopenId'].id}