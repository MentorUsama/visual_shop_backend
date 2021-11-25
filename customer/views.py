from rest_framework.response import Response
from .serializer import RegisterSerializer
from .models import Customer

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
            data={"has_error":False,"message":"Signup Successfully","email":customer.email}
        else:
            data={"has_error":True,"message":"Failed To Register. Please Enter the right Information"}
        return Response(data)



# Login API
@api_view(['GET','POST'])
@permission_classes((permissions.AllowAny,))
def LoginAPI(request):
    print("SDsdsd")
    if request.method=="POST":
        user1={};
        try:
            user1=Customer.objects.get(email=request.data['email'],password=request.data['password'])
            user1={"message":"Successfully Loged in","email":request.data['email'],"has_error":False}
            return Response(user1)
        except:
            user1={"message":"User Not Found","email":request.data['email'],"has_error":True}
            return Response(user1)