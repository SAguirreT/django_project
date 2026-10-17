from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/basico/productos/', include('farmacia.api_generic_urls')),
    path('api/v1/', include('farmacia.api_urls')),
    path('', include('farmacia.urls')),
]
