from rest_framework import serializers
from .serializer import RegisterSerializer,LoginSerializer,profileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Customer
from django.http import Http404
# from rest_framework import BasicAuthentication
from visualshop.utility.request import SerilizationFailed,Success
# JWT imports
from rest_framework_simplejwt.views import TokenObtainPairView





class RegisterAPI(APIView):
    def post(self, request, format=None):
        serializer=RegisterSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Success(serializer.data)
        else:
            return SerilizationFailed(serializer.errors)



class LoginAPI(TokenObtainPairView):
    serializer_class = LoginSerializer



class CustomerProfile(APIView,IsAuthenticated):
    def get_object(self, pk):        
        try:
            return Customer.objects.get(user=pk)
        except Customer.DoesNotExist:
            raise Http404
            
    def get(self, request, format=None):
        user=request.user
        customer=self.get_object(user)
        serializer=profileSerializer(customer,many=False)
        return Success(serializer.data);
