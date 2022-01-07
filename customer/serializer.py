from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import City, Customer,Province
# import jwt
from rest_framework_simplejwt.tokens import RefreshToken
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
    password=serializers.CharField(max_length=100)
    class Meta:
        model = Customer
        fields=["email","password","authType"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
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
                customer=Customer.objects.create(user=user,authType=validated_data['authType'])
                return {
                    'email':validated_data['email'],
                    'password':validated_data['password']
                }
            except Exception as e:
                return e
        else:
            raise serializers.ValidationError(userserialize.errors)



# Login Serializer
class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        if "username" in attrs.keys():
            attrs['username']=attrs['username'].lower()
        data = super().validate(attrs)
        print("sd")
        self.user.username=self.user.username.lower()
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
        fields=['name','address','contact','cityId']

# All Cities Serializer
class citySerializer(serializers.ModelSerializer):
    class Meta:
        model=City
        fields=['name','id']
class ProvinceAndCitiesSerializer(serializers.ModelSerializer):
    cities=citySerializer(many=True)
    class Meta:
        model=Province
        fields='__all__'
