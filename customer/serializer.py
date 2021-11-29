from rest_framework import serializers
from .models import Customer


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields=["email","password"]
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = Customer
        fields=["password","email"]