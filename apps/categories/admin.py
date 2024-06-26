from django.contrib import admin

from apps.categories.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


admin.site.register(Category, CategoryAdmin)
