from django.contrib import admin
from .models import Customer, Province, City
from django.contrib.auth.models import User


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name','city',)
    def city(self, obj: Customer):
        return obj.cityId


admin.site.register([Province, City])