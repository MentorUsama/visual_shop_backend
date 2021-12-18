from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('validateCuopen/<int:cupenCode>',views.ValidateCuopen.as_view(),name='validateCuopen'),
    path('createOrder/', views.CreateOrder.as_view(),name='createOrder'),
    path('getAllOrders/',views.GetAllOrders.as_view(),name="getAllOrders"),
    path('addComplaint/<int:orderId>',views.AddComplaint.as_view(),name="addComplaint"),
    path('sendMessage/<int:orderId>',views.AddMessage.as_view(),name="sendMessage")
]