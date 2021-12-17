from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('createOrder/', views.CreateOrder.as_view(),name='createOrder'),
]