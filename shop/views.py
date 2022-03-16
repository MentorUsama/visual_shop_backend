from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .serialization import ProductSerializer,GetAllTagSerializer,GetAllCategoriesSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from django.db.models import Count
# getting models
from shop.models.Product import Product
from shop.models.Tags import Tags
from shop.models.Category import Category
# from rest_framework import BasicAuthentication
from visualshop.utility.request import Success,SerilizationFailed
# Create your views here.


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000
class AllDataPagination(PageNumberPagination):
    page_size = None
    page_size_query_param = 'page_size'


class GetProductsAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class GetProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class GetProductByCategory(ListAPIView):
    serializer_class = ProductSerializer
    model = Product
    pagination_class = ProductPagination

    def get_queryset(self):
        uid = self.kwargs.get('pk')
        queryset = self.model.objects.filter(subCategoryId__categoryId=uid)
        return queryset


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
class FilterProduct(APIView):
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



class GetAllTags(ListAPIView):
    queryset =  Tags.objects.annotate(nused=Count('product')).order_by('-nused')
    serializer_class = GetAllTagSerializer
    pagination_class= AllDataPagination

class GetAllCategories(ListAPIView):
    queryset =  Category.objects.all()
    serializer_class = GetAllCategoriesSerializer
    pagination_class= AllDataPagination

class GetListOfProducts(APIView):
    def post(self, request, format=None):
        data = request.data
        if not "productIdList" in data.keys():
            return SerilizationFailed({"productIdList":"Please Provide The List Of Product To Fetch"})
        products=Product.objects.filter(id__in=data['productIdList'])
        serializer=ProductSerializer(products,many=True,context={'request': request})
        return Success(serializer.data)

class SearchByImage(APIView):
    def post(self,request,format=None):
        if 'image' not in request.FILES:
            return SerilizationFailed({"productIdList":"Please provide image"})
        print(request.FILES['image'])
        return Success("ok")