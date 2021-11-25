from django.contrib import admin
from .models import Cuopen,Order,Messages,OrderedProduct



class OrderedAdminInline(admin.TabularInline):
    model=OrderedProduct
    extra=1
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderedAdminInline]

admin.site.register([Cuopen])
# Register your models here.