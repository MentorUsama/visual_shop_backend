from rest_framework import serializers
from .serializer import RegisterSerializer,LoginSerializer,profileSerializer,profileUpdateSerializer,UserPasswordSerializer,ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Customer
from django.contrib.auth.models import User
from django.http import Http404
# Reset password libraries
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
# from rest_framework import BasicAuthentication
from visualshop.utility.request import SerilizationFailed,Success,NotFound
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

    def put(self, request, format=None):
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



# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@visualshop.local",
#         # to:
#         [reset_password_token.user.email]
#     )