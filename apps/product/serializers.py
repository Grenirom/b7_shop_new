from rest_framework import serializers
from .models import Product, ProductImage, ProductSize, ProductDiscount


class BaseProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    def get_discounted_price(self, obj):
        try:
            product_discount = ProductDiscount.objects.get(product=obj.id)
            discounted_price = obj.price - (obj.price * product_discount.discount / 100)
            return discounted_price
        except ProductDiscount.DoesNotExist:
            return None


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ('size', )


class ProductDetailSerializer(BaseProductSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    product_sizes = ProductSizeSerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'article', 'price', 'quantity', 'description',
                  'tech_characteristics', 'category', 'dop_info', 'images', 'product_sizes', 'stock',
                  'discounted_price']


class ProductListSerializer(BaseProductSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'images', 'article', 'title', 'price', 'stock',
                  'category','description', 'tech_characteristics', 'discounted_price')

