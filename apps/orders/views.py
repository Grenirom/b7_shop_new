from rest_framework import generics, permissions

from .models import Order
from .serializers import OrderSerializer
from . import permissions as my_permissions


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [my_permissions.IsAuthorOrAdmin, ]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.select_related('user').prefetch_related('items__product').filter(user=user)
        return queryset


# class OrderDetailView(generics.RetrieveAPIView):
