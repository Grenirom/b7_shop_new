from django.urls import path
from .views import ProductList, ProductDetail

urlpatterns = [
    path('list/', ProductList.as_view()),
    path('detail/<int:pk>/', ProductDetail.as_view()),
]