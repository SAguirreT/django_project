from rest_framework import generics

from .models import Producto
from .serializers import ProductoSerializer


class ProductoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.select_related('categoria').all()
    serializer_class = ProductoSerializer


class ProductoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.select_related('categoria').all()
    serializer_class = ProductoSerializer
