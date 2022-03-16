from rest_framework.generics import ListAPIView
from shop.serialization import ProductSerializer
from shop.models.Product import Product
from shop.views.product_pagination import ProductPagination
class GetProductByCategory(ListAPIView):
    serializer_class = ProductSerializer
    model = Product
    pagination_class = ProductPagination

    def get_queryset(self):
        uid = self.kwargs.get('pk')
        queryset = self.model.objects.filter(subCategoryId__categoryId=uid)
        return queryset
        