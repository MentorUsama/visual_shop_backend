from django.contrib import admin
from customer.models.Customer import Customer
from customer.models.Province import Province
from customer.models.City import City
from django.contrib.auth.models import User


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name','city',)
    def city(self, obj: Customer):
        return obj.cityId

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    