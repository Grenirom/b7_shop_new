from django.urls import path
from apps.categories import views

urlpatterns = [
    path('list/', views.CategoryListView.as_view()),
    path('detail/<int:pk>/', views.CategoryDetailView.as_view()),
]