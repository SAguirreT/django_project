from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalogo.api_views import ProductoViewSet
from pedidos.api_views import crear_pedido

router = DefaultRouter()
router.register('productos', ProductoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/pedidos/', crear_pedido, name='crear-pedido'),
    path('api/', include(router.urls)),
]
