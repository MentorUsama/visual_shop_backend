from rest_framework.response import Response
from rest_framework import status

def MethodNotAllowed():
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
def SerilizationFailed(data):
    return Response(data,status=status.HTTP_400_BAD_REQUEST)
def FailedVerification(data):
    return Response(data,status=status.HTTP_404_NOT_FOUND)
def Success(data):
    return Response(data)
    