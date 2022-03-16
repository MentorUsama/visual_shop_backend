from rest_framework.generics import ListAPIView
from shop.serialization import ProductSerializer
from shop.models.Product import Product
from shop.views.product_pagination import ProductPagination


class GetProductBySubCategory(ListAPIView):
    serializer_class = ProductSerializer
    model = Product
    pagination_class = ProductPagination

    def get_queryset(self):
        category = self.kwargs.get('category')
        subcategory = self.kwargs.get('subcategory')
        queryset = self.model.objects.filter(
            subCategoryId=subcategory, subCategoryId__categoryId=category)
        return queryset
        