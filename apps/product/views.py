from django.db.models import Prefetch, Subquery, OuterRef
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from .models import Product, ProductDiscount
from .serializers import ProductDetailSerializer, ProductListSerializer


class StandartResultPagination(PageNumberPagination):
    page_size = 4
    page_query_param = 'page'


class ProductListViewSet(ModelViewSet):
    pagination_class = StandartResultPagination
    queryset = Product.objects.annotate(
        discounted_price=Subquery(
            ProductDiscount.objects.filter(product=OuterRef('pk')).values('discount')[:1]
        )
    ).prefetch_related(
        'images'
    ).all().order_by('id')
    search_fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        if category_id is not None and category_id != '':
            queryset = queryset.filter(category=category_id)

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
