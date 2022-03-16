from shop.models.Tags import Tags
from rest_framework.generics import ListAPIView
from django.db.models import Count
from shop.serialization import GetAllTagSerializer
from shop.views.all_data_pagination import AllDataPagination
class GetAllTags(ListAPIView):
    queryset =  Tags.objects.annotate(nused=Count('product')).order_by('-nused')
    serializer_class = GetAllTagSerializer
    pagination_class= AllDataPagination