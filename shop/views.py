from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .serialization import ProductSerializer
from rest_framework.generics import ListAPIView
# getting models
from .models import Product
# Create your views here.
class ProductPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10000



class GetProductsAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination