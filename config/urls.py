from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/categories/', include('apps.categories.urls')),
    path('api/products/', include('apps.product.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/account/', include('apps.account.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)