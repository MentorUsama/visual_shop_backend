from shop.serialization import ProductSerializer
from shop.models.Product import Product
from rest_framework.generics import RetrieveAPIView


class GetProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer