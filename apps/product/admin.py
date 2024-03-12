from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


# class ProductSizeInline(admin.TabularInline):
#     model = ProductSize
#     extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
    }
    list_display = ('title', 'article', 'price', 'quantity', 'category', 'stock')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
