from django.contrib import admin
from django.db.models import fields
from .models import Cuopen,Order,Messages,Complaints,OrderedProduct



class OrderedAdminInline(admin.TabularInline):
    model=OrderedProduct
    extra=1
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    inlines=[OrderedAdminInline]


class MessageAdminInline(admin.TabularInline):
    model=Messages
    readonly_fields=("isAdmin","date")
    extra=1
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
@admin.register(Complaints)
class ComplaintsAdmin(admin.ModelAdmin):
    inlines=[MessageAdminInline]
    fields=("orderId","complaintStatus")
    readonly_fields=("orderId",)
    list_display = ('complaintStatus', 'Order_Detail','last_message_date')
    def Order_Detail(self, obj: Complaints):
        return obj.orderId
    def last_message_date(self, obj: Complaints):
        lastMessage= Messages.objects.filter(complainId=obj.id).latest()
        print(lastMessage)
        return f'{lastMessage.date}'



@admin.register(Cuopen)
class CuopenAdmin(admin.ModelAdmin):
    list_display = ('cuopenCode','totalQuantity','expiryDate','minPurchase')


admin.site.register([])
# Register your models here.