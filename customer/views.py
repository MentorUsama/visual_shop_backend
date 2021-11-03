from rest_framework.response import Response
from .serializer import RegisterSerializer
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

# from rest_framework import BasicAuthentication
from .serializer import RegisterSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view,permission_classes

# Register API
@api_view(['GET','POST'])
@permission_classes((permissions.AllowAny,))
def RegisterAPI(request):
    if request.method=="POST":
        serializer=RegisterSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            customer=serializer.save()
            print(customer)
            data['response']='Successfully Created the user'
            data['email']=customer.email
        else:
            data=serializer.errors
        return Response(data)