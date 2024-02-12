from rest_framework import serializers
from .models import Product, ProductImage, ProductSize, ProductDiscount


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ('size', )


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    product_sizes = ProductSizeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'article', 'price', 'quantity', 'description',
                  'tech_characteristics', 'category', 'dop_info', 'images', 'product_sizes', 'stock']


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'images', 'title', 'price', 'stock',
                  'category', 'discounted_price')

    def get_discounted_price(self,  obj):
        try:
            product_discount = ProductDiscount.objects.get(product=obj.id)
            discounted_price = obj.price - (obj.price * product_discount.discount / 100)
            return discounted_price
        except ProductDiscount.DoesNotExist:
            return None
