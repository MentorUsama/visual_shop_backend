from rest_framework.pagination import PageNumberPagination
class AllDataPagination(PageNumberPagination):
    page_size = None
    page_size_query_param = 'page_size'