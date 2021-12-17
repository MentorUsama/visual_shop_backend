from rest_framework.views import APIView
from  .serializer import OrderSerializer,OrderedProductSerializer
from customer.models import Customer
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
# from rest_framework import BasicAuthentication
from visualshop.utility.request import SerilizationFailed,Success,NotFound

# Create your views here.
class CreateOrder(APIView,IsAuthenticated):
    def get_object(self, pk):        
        try:
            customer=Customer.objects.get(user=pk)
            return customer
        except Customer.DoesNotExist:
            raise Http404
    def post(self, request, format=None):
        # Passed Data
        data=request.data

        # Getting the Customer
        user=request.user
        customer=self.get_object(user)
        data['customerId']=customer.id
        
        # Getting the order
        order=OrderSerializer(data=data)
        if(order.is_valid()):
            return Success(order.data)
        else:
            return SerilizationFailed(order.errors)