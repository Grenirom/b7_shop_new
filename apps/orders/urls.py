from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.OrderCreateView.as_view()),
    path('list/', views.OrderListView.as_view()),
]
