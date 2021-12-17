from rest_framework.views import APIView
from  .serializer import OrderSerializer
# from rest_framework import BasicAuthentication
from visualshop.utility.request import SerilizationFailed,Success,NotFound

# Create your views here.
class CreateOrder(APIView):
    def post(self, request, format=None):
        order=OrderSerializer(data=request.data)
        if(order.is_valid()):
            return Success(order.data)
        else:
            return SerilizationFailed(order.errors)