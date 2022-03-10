from django.contrib import admin
from django.db import models
from django.utils.html import escape
from django.utils.html import mark_safe

from shop.models.Category import Category
from shop.models.SubCategory import SubCategory
from shop.models.Tags import Tags
from shop.models.Product import Product
from shop.models.Images import Images

from django_rest_passwordreset.models import ResetPasswordToken
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

# ===================== Product with different Inlines ===========================
class ImageAdminInline(admin.TabularInline):
    model=Images
    extra=1
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
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id','name')

admin.site.unregister(ResetPasswordToken)
admin.site.unregister(Group)
admin.site.unregister(User)
