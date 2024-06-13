from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Product, ProductImage, ProductHome, ProductTechImages, ProductTechCharacteristics, MainPage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductTechImageInline(admin.TabularInline):
    model = ProductTechImages
    extra = 8


class ProductTechCharInline(admin.TabularInline):
    model = ProductTechCharacteristics
    extra = 8


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductTechImageInline, ProductTechCharInline]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 80})},
    }
    list_display = ('title', 'article', 'price', 'quantity', 'category', 'stock')
    list_select_related = ('category',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('category').prefetch_related('images', 'tech_images')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductHome)
admin.site.register(MainPage)