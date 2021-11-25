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



# class LoginSerializer(serializers.Serializer):
#     email=serializers.EmailField(max_length=50,unique=True)
#     password=serializers.CharField(max_length=100,null=False)

#     def save(self, validated_data):
#         user1={};
#         try:
#             user1=Customer.objects.get(email="usama.farhat.99@gmail.com",password="password")
#             user1={"message":"Successfully Loged in","email":validated_data['email'],"has_error":False}
#             return user1;
#         except:
#             user1={"message":"User Not Found","email":validated_data['email'],"has_error":True}
#             return user1;