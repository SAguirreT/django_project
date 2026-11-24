from django.db.models.deletion import ProtectedError
from rest_framework import filters, serializers, viewsets

from .models import Producto
from .serializers import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('categoria')
    serializer_class = ProductoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'categoria__nombre']

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as error:
            raise serializers.ValidationError('El producto tiene pedidos asociados.') from error
