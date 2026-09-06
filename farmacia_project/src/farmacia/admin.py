from django.contrib import admin

from .models import Categoria, Cliente, Producto, Proveedor, Venta

admin.site.register([Categoria, Producto, Proveedor, Cliente, Venta])

# Admin disabled by requirement: data stays in memory and no Django Admin should manage it.
