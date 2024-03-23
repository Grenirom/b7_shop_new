from django.urls import path
from .views import ProductList, ProductDetail, ProductListWithNoChild

urlpatterns = [
    path('list/', ProductList.as_view()),
    path('detail/<int:pk>/', ProductDetail.as_view()),
    path('list_no_child/', ProductListWithNoChild.as_view()),
]