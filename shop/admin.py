from django.contrib import admin
from django.db import models
from django.utils.html import escape
from django.utils.html import mark_safe
from .models import Category,SubCategory,Tags,Product,Images




# ===================== Product with different Inlines ===========================
class ImageAdminInline(admin.TabularInline):
    model=Images
    extra=1
# class FeedbackInline(admin.TabularInline):
#     model=Feedback
#     extra=1
#     def has_add_permission(self, request, obj=None):
#         return True
#     def has_delete_permission(self, request, obj=None):
#         return True
#     def has_change_permission(self, request, obj=None):
#         return True
    # def get_readonly_fields(self, request, obj=None):
    #     return list(super().get_fields(request, obj))

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Image','name','quantity','price','Category','SubCategory','sizes')
    inlines=[ImageAdminInline]
    # Extra Field
    def Category(self, obj: Product):
        return obj.subCategoryId.categoryId
    def SubCategory(self, obj: Product):
        return obj.subCategoryId
    def Image(self, obj: Product):
        try:
            firstImage=Images.objects.filter(productId=obj.id)[0].image
            return mark_safe(u'<img src="%s" width="50px"  />' % escape(firstImage.url))
        except:
            return "Not Found"
# ===================== Registering the rest of the table =========================
admin.site.register([Category,SubCategory,Tags])