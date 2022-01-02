from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    # Authentication Related API's
    path('auth/register', views.RegisterAPI.as_view(),name='register'),
    path('auth/login', views.LoginAPI.as_view(), name='login'),
    path('auth/google',views.GoogleLoginRegister.as_view(),name="google_login"),
    path('auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # Profile Related API
    path('profile/customerProfile', views.CustomerProfile.as_view(),name='CustomerProfile'),
    path('profile/updatePassword', views.UserUpdatePasswordAPI.as_view(),name='updatePassword'),
    path('getProvinceAndCities',views.GetProvinceAndCities.as_view(),name="getProvinceAndCities")
]