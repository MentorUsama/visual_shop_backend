from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from  .serializer import MessageSerializer, ValidateOrderSerializer,CheckOrderSerializer,GetAllOrdersSerializer,CreateComplaintsSerializer,AddFeedbackSerializer,ComplaintsSerializer
from customer.models.Customer import Customer
from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from orders.models.Cuopen import Cuopen
from orders.models.Order import Order
from orders.models.Complaints import Complaints
from orders.models.OrderedProduct import OrderedProduct
from orders.models.Messages import Messages

from shop.models.Product import Product
from shop.serialization import ProductSerializer
from visualshop.settings import STRIPE_SECRET_KEY
import stripe
stripe.api_key=STRIPE_SECRET_KEY
from orders.models.stripe import Stripe
# from rest_framework import BasicAuthentication
from visualshop.utility.request import SerilizationFailed,Success,NotFound,unAuthrized

# Create your views here.
def TotalPrice(orderedProducts):
    total=0
    for orderedProduct_data in orderedProducts:
        price=orderedProduct_data['totalQuantity']*orderedProduct_data['productId'].price
        total=total+price
    return total
class CreateOrder(APIView,IsAuthenticated):
    def get_object(self, pk):        
        try:
            customer=Customer.objects.get(user=pk)
            return customer
        except Customer.DoesNotExist:
            raise Http404
    def post(self, request, format=None):
        if(request.user.is_anonymous):
            return unAuthrized({"detail":"You are not Autherized to access"})

        # Passed Data
        data=request.data

        # Getting the Customer
        user=request.user
        customer=self.get_object(user)
        data['customerId']=customer.id

        # Checking if the coupen was used by customer before
        if 'cuopenId' in data:
            if data['cuopenId']!=None:
                order_with_given_coupen=Order.objects.filter(cuopenId__id=data['cuopenId'],customerId=customer)
                if len(order_with_given_coupen) != 0:
                    return SerilizationFailed({"cuopenCode":["This coupen has already been used"]})

        # validating the order data
        serialized_order=ValidateOrderSerializer(data=data)

        if(serialized_order.is_valid()):
            # Getting the validated data (Note: below line will not save the data in DB)
            validated_data=serialized_order.save()

            # Getting the ordered Products
            ordered_products = validated_data.pop('orderedProducts')

            # Calculating the Total Price
            orderPrices=TotalPrice(ordered_products)

            # Applying the coupen
            if(validated_data['cuopenId']!=None):
                if(orderPrices<validated_data['cuopenId'].minPurchase):
                    return SerilizationFailed({"cuopenId":["Total Purchase must be greater then "+str(validated_data['cuopenId'].minPurchase)+""]})
                discout=(validated_data['cuopenId'].discountPercentage*orderPrices)/100
                orderPrices=orderPrices-discout
                validated_data['cuopenId'].totalQuantity=validated_data['cuopenId'].totalQuantity-1
                validated_data['cuopenId'].save()

            # Setting up some field based on order type
            if validated_data['paymentMethod']=="CARD":
                orderStatus='Payment_pending'
                intent = stripe.PaymentIntent.create(
                    amount=int(orderPrices*100),
                    currency='USD',
                    automatic_payment_methods={'enabled': True,},
                ) 
                strip = Stripe.objects.create(strip_client_id=intent['id'],stripe_client_secret=intent['client_secret'])
            elif validated_data['paymentMethod']=="CASH":
                orderStatus='packaging'
                strip=None

            # Creating The order
            order = Order.objects.create(**validated_data,totalPrice=orderPrices,orderStatus=orderStatus,stripe=strip)
           
            # Creating the orderedProduct
            for (orderedProduct_data) in (ordered_products):
                totalPrice=orderedProduct_data['productId'].price*orderedProduct_data['totalQuantity']
                OrderedProduct.objects.create(orderId=order, **orderedProduct_data,totalPrice=totalPrice)
            
            # Decreasing The quantity of product as it has been purchased
            for (orderedProduct_data) in (ordered_products):
                product=orderedProduct_data['productId']
                product.quantity=product.quantity-orderedProduct_data['totalQuantity']
                product.save()
            response=GetAllOrdersSerializer(order)
            return Success(response.data)
        else:
            return SerilizationFailed(serialized_order.errors)
class ConfirmOrderPayment(APIView,IsAuthenticated):
    def get_object(self, pk):        
        try:
            customer=Customer.objects.get(user=pk)
            return customer
        except Customer.DoesNotExist:
            raise Http404
    def post(self, request, format=None):
        if(request.user.is_anonymous):
            return unAuthrized({"detail":"You are not Autherized to access"})
        # Passed Data
        data=request.data
        user=request.user
        customer=self.get_object(user)
        if 'order_id' not in data:
            return SerilizationFailed({'order_id':['Please provide valid order_id']})
        try:
            order=Order.objects.get(id=data['order_id'],customerId=customer.id,paymentMethod="CARD")
        except Order.DoesNotExist:
            return SerilizationFailed({'order_id':['Please provide valid order_id']})

        intent = stripe.PaymentIntent.retrieve(
            order.stripe.strip_client_id
        )
        if intent['status']=='succeeded':
            if order.orderStatus=='Payment_pending':
                order.orderStatus='packaging'
                order.save()
            return Success({'status':"packaging"})
        else:
            return Success({'status':order.orderStatus})

class CancelOrderPayment(APIView,IsAuthenticated):
    def get_object(self, pk):        
        try:
            customer=Customer.objects.get(user=pk)
            return customer
        except Customer.DoesNotExist:
            raise Http404
    def post(self, request, format=None):
        if(request.user.is_anonymous):
            return unAuthrized({"detail":"You are not Autherized to access"})
        # Passed Data
        data=request.data
        user=request.user
        customer=self.get_object(user)
        if 'order_id' not in data:
            return SerilizationFailed({'order_id':['Please provide valid order_id']})
        try:
            order=Order.objects.get(id=data['order_id'],customerId=customer.id)
        except Order.DoesNotExist:
            return SerilizationFailed({'order_id':['Please provide valid order_id']})

        if order.orderStatus=='Payment_pending' and order.paymentMethod=='CARD':# If the product is not purchased yet then you can cancel it.
            # Checking if the order is purchased or not from the stripe side
            intent = stripe.PaymentIntent.retrieve(
                order.stripe.strip_client_id
            )
            if intent['status']=='requires_payment_method': # if not purchased
                order.orderStatus='canceled'
                order.save()
                return Success({'status':"cannceled"})
            else:
                if intent['status']=='succeeded':
                    order.orderStatus='shipping'
                    order.save()
                return SerilizationFailed({'order_id':['You can not cancel the product which is already purchased or payment in progress.']})
        elif order.orderStatus=='packaging' and order.paymentMethod=='CASH': # if the product purchase method is cash and it is in packaging mode then you can not cacel it
            order.orderStatus='canceled'
            order.save()
            return Success({'status':"cannceled"})
        else:
            return SerilizationFailed({'order_id':['You can not cancel the product which is already purchased or payment in progress.']})

class ValidateCuopen(APIView,IsAuthenticated):
    def get_object(self, pk):        
        try:
            cuopen=Cuopen.objects.get(cuopenCode=pk)
            return cuopen
        except Cuopen.DoesNotExist:
            raise Http404
    def get_customer(self, pk):        
        try:
            customer=Customer.objects.get(user=pk)
            return customer
        except Customer.DoesNotExist:
            raise Http404
    def post(self,request,cupenCode):
        # validating the customer
        if(request.user.is_anonymous):
            return unAuthrized({"detail":"You are not Autherized to access"})
        user=request.user
        try:
            customer=self.get_customer(user)
        except Http404:
            return unAuthrized({"detail":"No customer found with given credential"})

        # Getting the cuopen
        try:
            cupen=self.get_object(cupenCode)
        except Http404:
            return SerilizationFailed({"cuopenCode":["No Coupen Found"]})

        # Checking if the coupen was used by customer before
        order_with_given_coupen=Order.objects.filter(cuopenId=cupen,customerId=customer)
        if len(order_with_given_coupen) != 0:
            return SerilizationFailed({"cuopenCode":["This coupen has already been used"]})

        # Checking the cuopen
        data=request.data
        data['cuopenId']=cupen.id
        serilizedData=CheckOrderSerializer(data=request.data)
        if(serilizedData.is_valid()):
            result=serilizedData.save()
            return Success(result)
        else:
            return SerilizationFailed(serilizedData.errors)
class OrdersPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000
class AllDataPagination(PageNumberPagination):
    page_size = None
    page_size_query_param = 'page_size'
class GetAllOrders(ListAPIView,IsAuthenticated):
    serializer_class = GetAllOrdersSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = AllDataPagination
    def get_object(self, pk):        
        try:
            customer=Customer.objects.get(user=pk)
            return customer
        except Customer.DoesNotExist:
            raise Http404
    def get_queryset(self):
        user = self.request.user
        customer=self.get_object(user)
        return Order.objects.filter(customerId=customer.id)
class ComplaintView(APIView,IsAuthenticated):
    def get_object(self, user,orderId):        
        try:
            order=Order.objects.get(customerId__user=user,id=orderId)
            return order
        except Order.DoesNotExist:
            raise Http404
    def get_Customer(self, pk):        
        try:
            customer=Customer.objects.get(user=pk)
            return customer
        except Customer.DoesNotExist:
            raise Http404
    def post(self,request,orderId):
        if(request.user.is_anonymous):
            return unAuthrized({"detail":"You are not Autherized to access"})
        user=request.user
        try:
            order=self.get_object(user,orderId)
        except Http404:
            return NotFound({"detail":"Order not Found"})
        complaintSerializer=CreateComplaintsSerializer(data={"orderId":orderId})
        if(complaintSerializer.is_valid()):
            complaintSerializer.save()
            return Success(complaintSerializer.data);
        else:
            return SerilizationFailed(complaintSerializer.errors)
        
    def get(self,request):
        parameters = request.GET.dict()
        user = request.user
        if 'complaint_id' not in parameters:
            return SerilizationFailed({'complaint_id':['Please provide complaint id to get detail']})
        customer=self.get_Customer(user)
        try:
            complaints = Complaints.objects.get(id=parameters['complaint_id'],orderId__customerId=customer)
        except:
            return SerilizationFailed({'complaint_id':['Complaint not found']})
        serialized_data = ComplaintsSerializer(complaints)
        return Success(serialized_data.data)
class AddMessage(APIView,IsAuthenticated):
    def get_object(self, user,orderId):      
        try:
            complaint=Complaints.objects.get(orderId=orderId,orderId__customerId__user=user)
            return complaint
        except Complaints.DoesNotExist:
            raise Http404
    def post(self,request,orderId):
        if(request.user.is_anonymous):
            return unAuthrized({"detail":"You are not Autherized to access"})
        user=request.user
        try:
            complaint=self.get_object(user,orderId)
        except Http404:
            return NotFound({"detail":"Complaint not Found"})
        data=request.data
        data['complainId']=complaint.id
        data['isAdmin']=False
        messageSerializer=MessageSerializer(data=data)
        if(messageSerializer.is_valid()):
            messageSerializer.save()
            return Success(messageSerializer.data);
        else:
            return SerilizationFailed(messageSerializer.errors)

class ProvideFeedback(APIView,IsAuthenticated):
    def post(self,request):
        data=request.data
        if(request.user.is_anonymous):
            return unAuthrized({"detail":"You are not Autherized to access"})
        if data['productId']==None:
            return SerilizationFailed({"productId":"Please Provide Product Id"})

        # Submitting The Feedback
        submittedBy=request.user
        serializer=AddFeedbackSerializer(data=data)
        if(serializer.is_valid()):
            orderBy=OrderedProduct.objects.get(id=data['orderedProductId']).orderId.customerId.user.id
            if(orderBy!=submittedBy.id):
                return unAuthrized({"detail":"You Are Not Authorize To Submit Feedback"})
            serializer.save()
            # Getting The Product Detail
            product=Product.objects.get(id=data['productId'])
            prooductSerializer=ProductSerializer(product,context={'request': request})
            return Success(prooductSerializer.data)
        else:
            return SerilizationFailed(serializer.errors)