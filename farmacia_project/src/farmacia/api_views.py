from django.db.models.deletion import ProtectedError
from rest_framework import filters, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Categoria, EvaluacionUbicacion, Farmacia, Producto, Venta, Zona
from .ventas import eliminar_venta
from .serializers import (
    CategoriaSerializer, FarmaciaSerializer, ProductoSerializer, VentaReadSerializer,
    EvaluacionUbicacionSerializer, VentaWriteSerializer, ZonaSerializer,
)


class CatalogoViewSet(viewsets.ModelViewSet):
    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as error:
            raise serializers.ValidationError('El registro tiene relaciones protegidas.') from error


class CategoriaViewSet(CatalogoViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProductoViewSet(CatalogoViewSet):
    serializer_class = ProductoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion', 'categoria__nombre']
    ordering_fields = ['nombre', 'precio', 'stock']
    ordering = ['nombre']

    def get_queryset(self):
        queryset = Producto.objects.select_related('categoria')
        disponible = self.request.query_params.get('disponible')
        if disponible and disponible.lower() in {'true', '1', 'si', 'sí'}:
            queryset = queryset.con_stock()
        elif disponible and disponible.lower() in {'false', '0', 'no'}:
            queryset = queryset.filter(stock=0)
        return queryset

    @action(detail=False, methods=['get'], url_path='con-stock')
    def con_stock(self, request):
        productos = self.filter_queryset(self.get_queryset().con_stock())
        page = self.paginate_queryset(productos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(productos, many=True).data)


class FarmaciaViewSet(viewsets.ModelViewSet):
    serializer_class = FarmaciaSerializer
    queryset = Farmacia.objects.select_related('zona').all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'tipo', 'estado', 'zona__nombre_zona']
    ordering_fields = ['nombre', 'distancia_metros', 'estado']
    ordering = ['nombre']

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado__iexact=estado)
        return queryset


    @action(detail=False, methods=['get'])
    def activas(self, request):
        # Reutiliza el QuerySet y conserva búsqueda, ordenamiento y paginación.
        queryset = self.filter_queryset(self.get_queryset().activas())
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(queryset, many=True).data)


class VentaViewSet(viewsets.ModelViewSet):
    serializer_class = VentaReadSerializer
    queryset = Venta.objects.select_related('cliente').prefetch_related(
        'detalles__producto__categoria'
    )
    filter_backends = [filters.SearchFilter]
    search_fields = ['cliente__nombre', 'cliente__documento', 'detalles__producto__nombre']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VentaWriteSerializer
        return super().get_serializer_class()

    def perform_destroy(self, instance):
        eliminar_venta(instance.pk)


class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.order_by('nombre_zona', 'pk')
    serializer_class = ZonaSerializer


class EvaluacionUbicacionReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EvaluacionUbicacionSerializer

    def get_queryset(self):
        # Carga evaluación y zona juntas para evitar una consulta por fila.
        return EvaluacionUbicacion.objects.select_related('zona').order_by('pk')
