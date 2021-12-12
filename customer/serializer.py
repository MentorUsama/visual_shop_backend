from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer
# import jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer






# Register Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        return User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
class ChangePasswordSerializer(serializers.ModelSerializer):
    model = User
    old_password = serializers.CharField(required=True)
    username=serializers.EmailField(required=True)
    class Meta:
        model=User
        fields=['password','old_password','username']
class RegisterSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    password=serializers.CharField(max_length=29)
    class Meta:
        model = Customer
        fields=["email","password"]
    def create(self, validated_data):
        # Creating the user
        userserialize=UserSerializer(data={
            'email':validated_data['email'],
            'username':validated_data['email'],
            'password':validated_data['password']
        })
        if(userserialize.is_valid()):
            user=User.objects.create_user(validated_data['email'],validated_data['email'],validated_data['password'])
            try:
                customer=Customer.objects.create(user=user)
                return {
                    'email':validated_data['email'],
                    'username':validated_data['email'],
                    'password':validated_data['password']
                }
            except Exception as e:
                return e
        else:
            raise serializers.ValidationError(userserialize.errors)



# Login Serializer
class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username']=self.user.username
        return data



# Profile Data Serializer
class profileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Customer
        depth=2
        fields='__all__'
class profileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['name','address','contact','jazzCashNumber','cardNumber','cardExpiryDate','CVC','cityId']