from rest_framework import serializers
from .models import Product, ProductImage


class BaseProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    def get_discounted_price(self, obj):
        if obj.discount is not None:
            discounted_price  = obj.price - (obj.price * obj.discount / 100)
            return discounted_price
        return None


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ChildProductSerializer(BaseProductSerializer):
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('price', 'article', 'optional_size', 'price', 'discounted_price', 'stock')


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(BaseProductSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField()
    various_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'article', 'price', 'quantity', 'description',
                  'tech_characteristics', 'category', 'dop_info', 'images', 'stock',
                  'various_products', 'discounted_price']

    def get_various_products(self, obj):
        children = obj.various_products.all()
        serializer = ChildProductSerializer(children, many=True)
        return serializer.data


class ProductListSerializer(BaseProductSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = ('id', 'images', 'article', 'title', 'price', 'stock',
                  'category','description', 'tech_characteristics', 'discounted_price')

