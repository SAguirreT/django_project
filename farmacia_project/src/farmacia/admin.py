from django.contrib import admin

from .models import (
    Categoria, Cliente, DetalleVenta, EvaluacionUbicacion, Farmacia,
    PerfilCliente, Producto, Proveedor, Venta, Zona,
)

admin.site.register([
    Categoria, Producto, Proveedor, Cliente, PerfilCliente, Venta, DetalleVenta,
    Zona, Farmacia, EvaluacionUbicacion,
])

# Admin disabled by requirement: data stays in memory and no Django Admin should manage it.
