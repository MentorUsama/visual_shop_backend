from django.contrib import admin
from django.db.models import fields
from .models import Cuopen, Order, Messages, Complaints, OrderedProduct


class OrderedAdminInline(admin.TabularInline):
    model = OrderedProduct
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_update_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','totalPrice','status','orderDate')
    readonly_fields = ('id','orderDate','totalPrice','shippingAddress','receiverName','receiverContact','cuopenId','customerId','cityId','strip_client_id','stripe_client_secret')
    inlines = [OrderedAdminInline]
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def status(self, obj):
        return obj.get_orderStatus_display()


class MessageAdminInline(admin.TabularInline):
    model = Messages
    readonly_fields = ("isAdmin", "date")
    extra = 1

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Complaints)
class ComplaintsAdmin(admin.ModelAdmin):
    inlines = [MessageAdminInline]
    fields = ("orderId", "complaintStatus")
    readonly_fields = ("orderId",)
    list_display = ('complaintStatus', 'Order_Detail', 'last_message_date')

    def Order_Detail(self, obj: Complaints):
        return obj.orderId

    def last_message_date(self, obj: Complaints):
        lastMessage = Messages.objects.filter(complainId=obj.id).latest()
        return f'{lastMessage.date}'
    def has_add_permission(self, request, obj=None):
            return False
    def has_delete_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Cuopen)
class CuopenAdmin(admin.ModelAdmin):
    list_display = ('cuopenCode', 'totalQuantity', 'expiryDate', 'minPurchase')


admin.site.register([])
# Register your models here.
