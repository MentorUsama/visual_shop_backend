from django.urls import path
from django.urls import path, include
# Getting all views
from shop.views.get_all_products import GetAllProducts
from shop.views.get_produt_detail import GetProductDetail
from shop.views.get_filter_product import GetFilteredProduct
from shop.views.get_all_tags import GetAllTags
from shop.views.get_all_category import GetAllCategories
from shop.views.get_list_of_products import GetListOfProducts
from shop.views.get_product_category import GetProductByCategory
from shop.views.get_product_by_subcategory import GetProductBySubCategory
from shop.views.get_product_by_text import GetProductByText
# from shop.views.get_product_by_image import GetProductByImage
from shop.core.signals.signal_images import auto_delete_file_on_change,auto_delete_file_on_delete,image_on_save


urlpatterns = [
    path('products/', GetAllProducts.as_view(),name='getProduct'),
    path('product/<pk>',GetProductDetail.as_view(),name="productDetail"),
    path('filterProducts',GetFilteredProduct.as_view(),name="FilterProduct"),
    path('getAllTags/',GetAllTags.as_view(),name="GetAllTags"),
    path('getAllCategories/',GetAllCategories.as_view(),name="GetAllCategories"),
    path('getListOfProducts/',GetListOfProducts.as_view(),name="getListOfProducts"),

    path('products/category/<pk>',GetProductByCategory.as_view(),name="getProductByCategory"),
    path('products/category/<category>/subcategory/<subcategory>',GetProductBySubCategory.as_view(),name="getProductBySubCategory"),
    path('products/search/<str:text>',GetProductByText.as_view(),name="GetProductByText"),
    # path('products/search-by-image',GetProductByImage.as_view(),name="SearchByImage")
]