from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('auth/register', views.RegisterAPI.as_view(),name='register'),
    path('auth/login', views.LoginAPI.as_view(), name='token_obtain_pair'),
    path('profile/customerProfile', views.CustomerProfile.as_view(),name='CustomerProfile'),
]