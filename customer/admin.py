from django.contrib import admin
from .models import Customer, Province, City


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','city')
    def city(self, obj: Customer):
        return obj.cityId


admin.site.register([Province, City])
# Register your models here.
