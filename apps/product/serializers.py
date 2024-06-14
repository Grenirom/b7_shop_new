from rest_framework import serializers
from .models import Product, ProductImage, ProductHome, ProductTechImages, ProductTechCharacteristics


class BaseProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    def get_discounted_price(self, obj):
        if obj.discount is not None:
            discounted_price = obj.price - (obj.price * obj.discount / 100)
            return discounted_price
        return None


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductTechImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTechImages
        fields = '__all__'


class ProductTechCharSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTechCharacteristics
        fields = '__all__'


class ChildProductSerializer(BaseProductSerializer):
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('price', 'article', 'optional_size', 'price', 'discounted_price', 'stock', 'product')


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(BaseProductSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    tech_images = ProductTechImageSerializer(many=True, read_only=True)
    tech_chars = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    various_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'article', 'price', 'quantity', 'description',
                  'tech_characteristics', 'category', 'dop_info', 'images', 'stock',
                  'optional_size', 'various_products', 'discounted_price', 'product',
                  'tech_chars', 'tech_images']

    def get_various_products(self, obj):
        children = obj.various_products.all()
        serializer = ChildProductSerializer(children, many=True)
        return serializer.data

    def get_tech_chars(self, obj):
        tech_chars = ProductTechCharacteristics.objects.all()
        serializer = ProductTechCharSerializer(tech_chars, many=True)
        return serializer.data


class ProductListSerializer(BaseProductSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'images', 'article', 'title', 'price', 'stock',
                  'category', 'description', 'tech_characteristics', 'discounted_price', 'product', 'discount',
                  'optional_size', 'main_page_category')


class ProductHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHome
        fields = '__all__'
        