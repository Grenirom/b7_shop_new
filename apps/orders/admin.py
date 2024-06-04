from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, ]

    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
    created_at_formatted.short_description = 'Дата создания заказа'

    list_display = ('user', 'created_at_formatted', 'name', 'phone_number', 'shipping_address', 'total_sum')


admin.site.register(Order, OrderAdmin)
