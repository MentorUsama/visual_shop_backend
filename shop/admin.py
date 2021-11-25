from django.contrib import admin
from django.db import models
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
    list_display = ('name','Category','SubCategory')
    inlines=[ImageAdminInline,FeedbackInline]
    def Category(self, obj: Product):
        return obj.subCategoryId.categoryId
    def SubCategory(self, obj: Product):
        return obj.subCategoryId
# ===================== Registering the rest of the table =========================
admin.site.register([Category,SubCategory,Tags,Images])