from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('validateCuopen/<int:cupenCode>',views.ValidateCuopen.as_view(),name='validateCuopen'),
    path('createOrder/', views.CreateOrder.as_view(),name='createOrder'),
]