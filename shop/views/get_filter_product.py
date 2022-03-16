from rest_framework.views import APIView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from shop.models.Product import Product
from shop.serialization import ProductSerializer
from visualshop.utility.request import Success
class GetFilteredProduct(APIView):
    def post(self, request, format=None):
        data = request.data
        if data['searchText'] != None:
            text = data['searchText']
            search_vector = SearchVector("tags__name", weight='A') + SearchVector('name', weight='B') + SearchVector('description', weight='C')
            search_query = SearchQuery(text)
            products = Product.objects.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
        else:
            products=Product.objects.all()
        if data['price'] != None:
            products = products.filter(
                price__gte=data['price'][0], price__lte=data['price'][1]).distinct()
        if data['tags'] != None:
            products = products.filter(tags__id__in=data['tags']).distinct()
        if data['subcategoryId'] != None:
            products = products.filter(subCategoryId=data['subcategoryId']).distinct()
        elif data['categoryId'] != None:
            products = products.filter(
                subCategoryId__categoryId=data['categoryId']).distinct()
        products=products.distinct()
        serializer=ProductSerializer(products,many=True,context={'request': request})
        return Success(serializer.data)
