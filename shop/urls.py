from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('products/', views.GetProductsAPI.as_view(),name='getProduct'),
    path('product/<pk>',views.GetProductDetail.as_view(),name="productDetail"),
    path('filterProducts',views.FilterProduct.as_view(),name="FilterProduct"),
    path('getAllTags/',views.GetAllTags.as_view(),name="GetAllTags"),
    path('getAllCategories/',views.GetAllCategories.as_view(),name="GetAllCategories"),
    path('getListOfProducts/',views.GetListOfProducts.as_view(),name="getListOfProducts"),

    path('products/category/<pk>',views.GetProductByCategory.as_view(),name="getProductByCategory"),
    path('products/category/<category>/subcategory/<subcategory>',views.GetProductBySubCategory.as_view(),name="getProductBySubCategory"),
    path('products/search/<str:text>',views.GetProductByText.as_view(),name="GetProductByText")
]