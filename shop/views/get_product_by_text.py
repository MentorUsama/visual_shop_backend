from rest_framework.generics import ListAPIView
from shop.models.Product import Product
from shop.serialization import ProductSerializer
from shop.views.product_pagination import ProductPagination
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


class GetProductByText(ListAPIView):
    serializer_class = ProductSerializer
    model = Product
    pagination_class = ProductPagination

    def get_queryset(self):
        text = self.kwargs.get('text')
        search_vector = SearchVector("tags__name", weight='A') + SearchVector(
            'name', weight='B') + SearchVector('description', weight='C')
        search_query = SearchQuery(text)
        results = Product.objects.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.3).order_by('-rank')
        return results