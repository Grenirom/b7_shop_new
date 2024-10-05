from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics

from rest_framework.pagination import PageNumberPagination

from .models import Product, ProductHome
from .serializers import ProductDetailSerializer, ProductListSerializer, ProductHomeSerializer

class ProductAbstract(generics.ListAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category=category_id)

        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(article__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tech_characteristics__icontains=search_query)
            )

        return queryset

    @method_decorator(cache_page(60 * 60))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ProductList(ProductAbstract):
    queryset = Product.objects.all().prefetch_related('images')
    serializer_class = ProductListSerializer


class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all().select_related('category').prefetch_related('images',
                                                                                 'tech_images')

    @method_decorator(cache_page(60 * 60))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductListWithNoChild(ProductAbstract):
    queryset = Product.objects.filter(product__isnull=True).prefetch_related('images')
    serializer_class = ProductListSerializer


class ProductHomeView(generics.ListAPIView):
    queryset = ProductHome.objects.all()
    serializer_class = ProductHomeSerializer

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
