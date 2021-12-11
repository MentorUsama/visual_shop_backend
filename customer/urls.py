from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('auth/register', views.RegisterAPI,name='register'),
    path('auth/login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]