from rest_framework.routers import DefaultRouter

from .api_views import (CategoriaViewSet, FarmaciaViewSet, ProductoViewSet, VentaViewSet,
                        ZonaViewSet, EvaluacionUbicacionReadOnlyViewSet)

router = DefaultRouter()
router.register('categorias', CategoriaViewSet, basename='api-categoria')
router.register('productos', ProductoViewSet, basename='api-producto')
router.register('farmacias', FarmaciaViewSet, basename='api-farmacia')
router.register('ventas', VentaViewSet, basename='api-venta')

router.register('zonas', ZonaViewSet, basename='api-zona')
router.register('evaluaciones', EvaluacionUbicacionReadOnlyViewSet, basename='api-evaluacion')

urlpatterns = router.urls
