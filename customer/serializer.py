from django.db.models.fields import EmailField
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('email', 'password')
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self):
        user=Customer(
            email=self.validated_data['email'],
            password=self.validated_data['password']
        )
        user.save()
        return user;