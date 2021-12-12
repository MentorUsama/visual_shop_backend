from rest_framework import serializers
from .serializer import RegisterSerializer,LoginSerializer,profileSerializer,profileUpdateSerializer,UserPasswordSerializer
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

    def put(self, request, format=None):
        user=request.user
        customer=self.get_object(user)
        serializer=profileUpdateSerializer(customer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Success(serializer.data)
        return SerilizationFailed(serializer.errors)

class UserUpdatePasswordAPI(APIView,IsAuthenticated):
    def put(self, request, format=None):
        user=request.user
        serializer=UserPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Success({"message":"Password has been updated"})
        return SerilizationFailed(serializer.errors)

class resetPasswordAPI(APIView):
    pass
    # """
    # An endpoint for changing password.
    # """
    # serializer_class = ChangePasswordSerializer
    # model = User
    # permission_classes = (IsAuthenticated,)

    # def get_object(self, queryset=None):
    #     obj = self.request.user
    #     return obj

    # def update(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     serializer = self.get_serializer(data=request.data)

    #     if serializer.is_valid():
    #         # Check old password
    #         if not self.object.check_password(serializer.data.get("old_password")):
    #             return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
    #         # set_password also hashes the password that the user will get
    #         self.object.set_password(serializer.data.get("new_password"))
    #         self.object.save()
    #         response = {
    #             'status': 'success',
    #             'code': status.HTTP_200_OK,
    #             'message': 'Password updated successfully',
    #             'data': []
    #         }

    #         return Response(response)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


