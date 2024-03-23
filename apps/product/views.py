from django.db.models import Q
from rest_framework import generics

from rest_framework.pagination import PageNumberPagination

from .models import Product
from .serializers import ProductDetailSerializer, ProductListSerializer


class StandartResultPagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'page'


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all().prefetch_related('images')
    serializer_class = ProductListSerializer

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


class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all().select_related('category').prefetch_related('images')


class ProductListWithNoChild(generics.ListAPIView):
    queryset = Product.objects.filter(product__isnull=True).prefetch_related('images')
    serializer_class = ProductListSerializer
    pagination_class = StandartResultPagination

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