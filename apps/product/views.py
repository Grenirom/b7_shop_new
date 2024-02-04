from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Product
from .serializers import ProductDetailSerializer, ProductListSerializer


class ProductListViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductDetailSerializer(instance)
        return Response(serializer.data)

    http_method_names = ['get', ]

