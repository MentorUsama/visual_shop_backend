from django.contrib import admin
from django.db import models
from django.utils.html import escape
from django.utils.html import mark_safe
from .models import Category,SubCategory,Tags,Product,Feedback,Images




# ===================== Product with different Inlines ===========================
class ImageAdminInline(admin.TabularInline):
    model=Images
    extra=1
class FeedbackInline(admin.StackedInline):
    model=Feedback
    extra=1
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Image','name','Category','SubCategory')
    inlines=[ImageAdminInline,FeedbackInline]
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
admin.site.register([Category,SubCategory,Tags,Images,Feedback])