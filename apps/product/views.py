from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Product
from .serializers import ProductDetailSerializer, ProductListSerializer


class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class ProductListViewSet(ModelViewSet):
    pagination_class = StandartResultPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    queryset = Product.objects.prefetch_related('images').all()
    search_fields = '__all__'

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = Product.objects.all().order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductDetailSerializer(instance)
        return Response(serializer.data)

    http_method_names = ['get', ]
