from orders.models.Complaints import Complaints
from orders.models.Messages import Messages
from orders.models.Order import Order
from orders.models.OrderedProduct import OrderedProduct
from orders.models.Complaints import Complaints
from orders.models.Feedback import Feedback
from datetime import date
from rest_framework import serializers
from shop.models.Product import Product
from shop.models.Images import Images
from customer.models.City import City
from customer.models.Province import Province





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
        fields=['id','totalPrice','shippingAddress','receiverName','receiverContact','cuopenId','customerId','cityId','orderedProducts','orderStatus','stripe_client_secret','strip_client_id']
        extra_kwargs = {
            'orderStatus': {'read_only': True},
            'strip_client_id':{"write_only":True} 
        }
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

# ============= Serializer For Getting All Orders =============
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
class SubcategorySerializer(serializers.ModelSerializer):
    categoryId = CategorySerializer
    class Meta:
        fields = "__all__"
class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'imageColor', 'image']
class ProductSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    subCategoryId = SubcategorySerializer
    
    class Meta:
        model = Product
        depth = 1
        fields = ['id','name','quantity','price','description','sizes','subCategoryId','images']


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Province
        fields=['name']
class CitySerializer(serializers.ModelSerializer):
    provinceId=ProvinceSerializer()
    class Meta:
        model=City
        fields=['name','provinceId']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Messages
        fields="__all__"
        extra_kwargs = {'complainId': {'write_only': True}, }
class ComplaintsSerializer(serializers.ModelSerializer):
    messages=MessageSerializer(many=True)
    class Meta:
        model=Complaints
        fields="__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id','rating','description']
class OrderedProductSerializer(serializers.ModelSerializer):
    feedback=FeedbackSerializer(many=False, read_only=True,source="feedbacks")
    productId=ProductSerializer(read_only=True)
    class Meta:
        model = OrderedProduct
        fields = ['id','feedback','totalQuantity','totalPrice','colourSelected','sizeSelected','productId']


class GetAllOrdersSerializer(serializers.ModelSerializer):
    cityId=CitySerializer()
    complaints=ComplaintsSerializer()
    orderedProducts = OrderedProductSerializer(many=True, read_only=True)
    class Meta:
        model=Order
        exclude = ('strip_client_id', )
# ============== Creating Complaint ========================
class CreateComplaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Complaints
        fields="__all__"
# ============== FeedbackSerializer ========================
class AddFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feedback
        fields="__all__"