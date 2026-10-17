from rest_framework.routers import DefaultRouter

from .api_views import CategoriaViewSet, FarmaciaViewSet, ProductoViewSet, VentaReadOnlyViewSet

router = DefaultRouter()
router.register('categorias', CategoriaViewSet, basename='api-categoria')
router.register('productos', ProductoViewSet, basename='api-producto')
router.register('farmacias', FarmaciaViewSet, basename='api-farmacia')
router.register('ventas', VentaReadOnlyViewSet, basename='api-venta')

urlpatterns = router.urls
