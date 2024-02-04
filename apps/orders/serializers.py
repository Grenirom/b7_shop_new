from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Order, OrderItem
from ..product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'product_title')


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    products = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['products'] = OrderItemSerializer(
            instance.items.all().select_related('product'), many=True
        ).data
        return repr

    def validate_products(self, products):
        product_ids = [product['product'].id for product in products]
        product_data_list = Product.objects.filter(id__in=product_ids)

        for product in products:
            product_id = product['product'].id
            product_data = next((p for p in product_data_list if p.id == product_id), None)

            if not product_data:
                raise serializers.ValidationError(f'Product with id {product_id} not found')

            if product_data.quantity < product['quantity']:
                raise serializers.ValidationError(f'Not enough quantity for {product_data.title}')

        return products

    @transaction.atomic
    def create(self, validated_data):
        products = validated_data.pop('products')
        user = self.context['request'].user
        total_sum = 0
        product_data_list = []

        for product in products:
            product_id = product['product'].id
            total_sum += product['quantity'] * product['product'].price

            product_data = get_object_or_404(Product, id=product_id)
            product_data.quantity -= product['quantity']
            product_data_list.append(product_data)

        Product.objects.bulk_update(product_data_list, ['quantity'])

        order = Order.objects.create(user=user, total_sum=total_sum, **validated_data)

        order_item_objects = [
            OrderItem(order=order,
                      product=product['product'],
                      quantity=product['quantity']) for product in products]
        OrderItem.objects.bulk_create(order_item_objects)

        return order
