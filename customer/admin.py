from django.contrib import admin
from .models import Customer, Province, City
from django.contrib.auth.models import User


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','email','name','city',)
    def city(self, obj: Customer):
        return obj.cityId
    def email(self, obj: Customer):
        return obj.user


admin.site.register([Province, City])