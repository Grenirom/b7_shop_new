from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, permissions

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = CategorySerializer

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = CategorySerializer

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
