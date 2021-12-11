from .serializer import RegisterSerializer,MyTokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import Customer

# from rest_framework import BasicAuthentication
from rest_framework import permissions
from rest_framework.decorators import api_view,permission_classes
from visualshop.utility.request import MethodNotAllowed,SerilizationFailed,Success
# JWT imports
from rest_framework_simplejwt.views import TokenObtainPairView





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
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer