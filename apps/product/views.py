from django.db.models import Avg, Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from .models import Product
from .serializers import ProductDetailSerializer, ProductListSerializer


class StandartResultPagination(PageNumberPagination):
    page_size = 8
    page_query_param = 'page'


class ProductListViewSet(ModelViewSet):
    pagination_class = StandartResultPagination
    queryset = Product.objects.annotate(
        avg_discount=Avg('product_discounts__discount')
    ).prefetch_related(
        'images',
        'product_discounts'
    ).order_by('id')

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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductDetailSerializer(instance)
        return Response(serializer.data)

    http_method_names = ['get', ]
