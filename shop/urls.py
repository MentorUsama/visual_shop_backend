from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('getProducts/', views.GetProductsAPI.as_view(),name='getProduct'),
]