from django.contrib import admin
from .models import Cuopen,Order,Messages,OrderedProduct



class OrderedAdminInline(admin.TabularInline):
    model=OrderedProduct
    extra=1
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderedAdminInline]

@admin.register(Cuopen)
class CuopenAdmin(admin.ModelAdmin):
    list_display = ('cuopenCode','totalQuantity','expiryDate','minPurchase')


admin.site.register([])
# Register your models here.