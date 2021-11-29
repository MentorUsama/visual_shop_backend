from .serializer import RegisterSerializer,LoginSerializer
from .models import Customer

# from rest_framework import BasicAuthentication
from rest_framework import permissions
from rest_framework.decorators import api_view,permission_classes
from visualshop.utility.request import MethodNotAllowed,SerilizationFailed,FailedVerification,Success



# Register API
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def RegisterAPI(request):
    if request.method=="POST":
        serializer=RegisterSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Success(serializer.data)
        else:
            return SerilizationFailed(serializer.errors)
    else:
        return MethodNotAllowed()



# Login API
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def LoginAPI(request):
    if request.method=="POST":
        serializer=LoginSerializer(data=request.data)
        if(serializer.is_valid()):
            try:
                customer = Customer.objects.get(email=serializer.data['email'])
                if customer.password==serializer.data['password']:
                    return Success({'message':"Loggedin Successfull",'email':serializer.data['email']})
                else:
                    return FailedVerification({'message':'Incorrect Email Or Password','email':serializer.data['email']})
            except Customer.DoesNotExist:
                return FailedVerification({'message':'Incorrect Email Or Password','email':serializer.data['email']})
        else:
            return SerilizationFailed(serializer.errors)
    else:
        return MethodNotAllowed()