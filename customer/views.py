from rest_framework import serializers
from .serializer import RegisterSerializer,LoginSerializer,profileSerializer,profileUpdateSerializer,ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Customer
from django.contrib.auth.models import User
from django.http import Http404
# from rest_framework import BasicAuthentication
from visualshop.utility.request import SerilizationFailed,Success,NotFound,unAuthrized
# JWT imports
from rest_framework_simplejwt.views import TokenObtainPairView
# Django Auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.utils import json
import requests





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





class GoogleLoginRegister(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return SerilizationFailed(content)

        # create user if not exist
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            password = make_password(BaseUserManager().make_random_password())
            serializationData={"email":data['email'],"password":password}
            serializationData['authType']="GOOGLE";
            serializer=RegisterSerializer(data=serializationData)
            if(serializer.is_valid()):
                serializer.save()
                user = User.objects.get(email=data['email'])
                user.set_unusable_password()
                user.save()
            else:
                return SerilizationFailed(serializer.errors)
        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Success(response)





class CustomerProfile(APIView,IsAuthenticated):
    def get_object(self, pk):        
        try:
            return Customer.objects.get(user=pk)
        except Customer.DoesNotExist:
            raise Http404
            
    def get(self, request, format=None):
        if(request.user.is_anonymous):
            return unAuthrized({"detail":"You are not Autherized to access"})
        user=request.user
        customer=self.get_object(user)
        serializer=profileSerializer(customer,many=False)
        return Success(serializer.data);

    def put(self, request, format=None):
        if(request.user.is_anonymous):
            return unAuthrized({"detail":"You are not Autherized to access"})
        user=request.user
        customer=self.get_object(user)
        serializer=profileUpdateSerializer(customer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Success(serializer.data)
        return SerilizationFailed(serializer.errors)





class UserUpdatePasswordAPI(APIView):
    def get_object(self, pk):        
        try:
            return User.objects.get(username=pk)
        except User.DoesNotExist:
            raise Http404
    def put(self, request, format=None):
        serializer=ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user=self.get_object(serializer.data['username'])
            except Http404:
                return NotFound({"message":"User with this email does not exist"})
            if user.check_password(serializer.data['old_password']):
                user.set_password(serializer.data['password'])
                user.save()
                return Success({"message":"Password has been updated"})
            else:
                return SerilizationFailed({"old_password":"Old password is incorrect"})
        return SerilizationFailed(serializer.errors)
