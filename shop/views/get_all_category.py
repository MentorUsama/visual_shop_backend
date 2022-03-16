import imp
from rest_framework.generics import ListAPIView
from shop.models.Category import Category
from shop.serialization import GetAllCategoriesSerializer
from shop.views.all_data_pagination import AllDataPagination
class GetAllCategories(ListAPIView):
    queryset =  Category.objects.all()
    serializer_class = GetAllCategoriesSerializer
    pagination_class= AllDataPagination