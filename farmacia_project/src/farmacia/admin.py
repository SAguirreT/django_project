from django.contrib import admin

from .models import (
    Categoria, Cliente, DetalleVenta, EvaluacionUbicacion, Farmacia,
    PerfilCliente, Producto, Proveedor, Venta, Zona,
)


class PerfilClienteInline(admin.StackedInline):
    model = PerfilCliente
    fields = ('direccion', 'observaciones')
    extra = 1
    max_num = 1


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    fields = ('producto', 'cantidad', 'precio_unitario')
    extra = 1


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('categoria',)
    list_select_related = ('categoria',)


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo')
    search_fields = ('nombre', 'correo')


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento', 'telefono', 'correo')
    search_fields = ('nombre', 'documento')
    inlines = (PerfilClienteInline,)


class PerfilClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'direccion', 'fecha_registro')
    search_fields = ('cliente__nombre', 'cliente__documento')
    list_filter = ('fecha_registro',)
    list_select_related = ('cliente',)


class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'total')
    search_fields = ('cliente__nombre', 'cliente__documento')
    list_filter = ('fecha',)
    list_select_related = ('cliente',)
    inlines = (DetalleVentaInline,)


class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('producto__nombre', 'venta__cliente__nombre')
    list_select_related = ('venta__cliente', 'producto')


# Registro explícito de las siete entidades de la investigación.
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(PerfilCliente, PerfilClienteAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta, DetalleVentaAdmin)

# Se conservan los modelos adicionales que ya estaban disponibles.
admin.site.register([Zona, Farmacia, EvaluacionUbicacion])
