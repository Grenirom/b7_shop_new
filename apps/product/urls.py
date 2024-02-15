from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'', views.ProductListViewSet, basename='products')

urlpatterns = [
    # path('filter/', views.ProductFilter.as_view()),
    path('', include(router.urls)),
]