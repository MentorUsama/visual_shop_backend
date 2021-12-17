from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('products/', views.GetProductsAPI.as_view(),name='getProduct'),
    path('product/<pk>',views.GetProductDetail.as_view(),name="productDetail"),
    path('products/category/<pk>',views.GetProductByCategory.as_view(),name="getProductByCategory"),
    path('products/category/<category>/subcategory/<subcategory>',views.GetProductBySubCategory.as_view(),name="getProductBySubCategory"),
    path('products/search/<str:text>',views.GetProductByText.as_view(),name="GetProductByText")
]