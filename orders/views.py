from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from  .serializer import MessageSerializer, OrderSerializer,CheckOrderSerializer,GetAllOrdersSerializer,CreateComplaintsSerializer,AddFeedbackSerializer
from customer.models import Customer
from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Cuopen,Order,Complaints, OrderedProduct
from shop.models import Product
from shop.serialization import ProductSerializer
from visualshop.settings import STRIPE_SECRET_KEY
import stripe
stripe.api_key=STRIPE_SECRET_KEY
# from rest_framework import BasicAuthentication
from visualshop.utility.request import SerilizationFailed,Success,NotFound,unAuthrized

# Create your views here.
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

        # Getting the order
        order=OrderSerializer(data=data)
        if(order.is_valid()):
            # Making The Payment
            intent = stripe.PaymentIntent.create(
                amount=100,
                currency='USD',
                automatic_payment_methods={'enabled': True,},
            )
            # Saving The Order
            data['stripe_client_secret'] = intent['client_secret']
            data['strip_client_id'] = intent['id']
            order_with_Strip=OrderSerializer(data=data)
            if order_with_Strip.is_valid():
                order_with_Strip.save()
                return Success(order_with_Strip.data)
            else:
                return SerilizationFailed(order_with_Strip.errors)
        else:
            return SerilizationFailed(order.errors)
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
            order=Order.objects.get(id=data['order_id'],customerId=customer.id)
        except Order.DoesNotExist:
            return SerilizationFailed({'order_id':['Please provide valid order_id']})

        intent = stripe.PaymentIntent.retrieve(
            order.strip_client_id
        )
        if intent['status']=='succeeded':
            order.orderStatus='shipping'
            order.save()
            return Success({'status':"shipping"})
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

        if order.orderStatus=='PAYMENTPENDING': # If the product is not purchased yet then you can cancel it.
            # Checking if the order is purchased or not from the stripe side
            intent = stripe.PaymentIntent.retrieve(
                order.strip_client_id
            )
            if intent['status']=='requires_payment_method': # if not purchased
                order.orderStatus='canceled'
                order.save()
                return Success({'status':"cannceled"})
            else:
                if intent['status']=='succeeded':
                    order.orderStatus='shipping'
                    order.save()
                return SerilizationFailed({'order_id':['You can not cancel the product which is already purchase shipped, canceled or payment in progress.']})
        else:
            return SerilizationFailed({'order_id':['You can not cancel the product which is already purchase shipped or canceled.']})

class ValidateCuopen(APIView):
    def get_object(self, pk):        
        try:
            cuopen=Cuopen.objects.get(cuopenCode=pk)
            return cuopen
        except Cuopen.DoesNotExist:
            raise Http404
    def post(self,request,cupenCode):
        try:
            cupen=self.get_object(cupenCode)
        except Http404:
            return SerilizationFailed({"cuopenCode":["No Coupen Found"]})
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
class AddComplaint(APIView,IsAuthenticated):
    def get_object(self, user,orderId):        
        try:
            order=Order.objects.get(customerId__user=user,id=orderId)
            return order
        except Order.DoesNotExist:
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