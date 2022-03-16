from rest_framework.generics import ListAPIView, RetrieveAPIView
from shop.models.Product import Product
from shop.serialization import ProductSerializer
from shop.views.product_pagination import ProductPagination
class GetAllProducts(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination