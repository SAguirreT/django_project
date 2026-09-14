from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from .models import Categoria, Cliente, DetalleVenta, PerfilCliente, Producto, Proveedor, Venta


class FarmaciaCrudTests(TestCase):
    def test_crud_y_relaciones(self):
        categoria = Categoria.objects.create(nombre='Analgésicos', descripcion='Control del dolor')
        producto = Producto.objects.create(nombre='Paracetamol', precio=Decimal('12.50'), stock=20, categoria=categoria)
        proveedor = Proveedor.objects.create(nombre='Distribuidora Andina', telefono='999999999', correo='ventas@andina.pe')
        cliente = Cliente.objects.create(nombre='Ana Torres', documento='12345678')
        venta = Venta.objects.create(cliente=cliente, fecha=timezone.make_aware(datetime(2026, 1, 1, 10, 0)), total=Decimal('12.50'))

        self.assertEqual(categoria.productos.get(), producto)
        self.assertEqual(cliente.ventas.get(), venta)
        producto.stock = 15
        producto.save()
        proveedor.delete()
        self.assertEqual(Producto.objects.get(pk=producto.pk).stock, 15)
        self.assertFalse(Proveedor.objects.filter(pk=proveedor.pk).exists())

    def test_productos_view_y_confirmacion_delete(self):
        categoria = Categoria.objects.create(nombre='Vitaminas')
        producto = Producto.objects.create(nombre='Vitamina C', precio=Decimal('20.00'), stock=10, categoria=categoria)
        self.assertEqual(self.client.get('/productos/').status_code, 200)
        confirmacion = self.client.get(f'/productos/{producto.pk}/eliminar/')
        self.assertContains(confirmacion, 'Confirmar eliminación')
        self.client.post(f'/productos/{producto.pk}/eliminar/')
        self.assertFalse(Producto.objects.filter(pk=producto.pk).exists())

    def test_relaciones_nuevas_y_crud_detalle_venta(self):
        categoria = Categoria.objects.create(nombre='Antigripales')
        producto = Producto.objects.create(nombre='Jarabe', precio=Decimal('18.00'), stock=8, categoria=categoria)
        cliente = Cliente.objects.create(nombre='Luis Ramos', documento='87654321')
        perfil = PerfilCliente.objects.create(cliente=cliente, direccion='Av. Lima 123')
        venta = Venta.objects.create(cliente=cliente, fecha=timezone.now(), total=Decimal('36.00'))

        self.assertEqual(cliente.perfil, perfil)
        detalle = DetalleVenta.objects.create(venta=venta, producto=producto, cantidad=2, precio_unitario=Decimal('18.00'))
        self.assertEqual(list(venta.productos.all()), [producto])
        self.assertEqual(detalle.subtotal, Decimal('36.00'))

        respuesta = self.client.get(f'/ventas/{venta.pk}/')
        self.assertContains(respuesta, 'Jarabe')
        self.assertEqual(self.client.get('/detalles-venta/').status_code, 200)

        self.client.post(
            f'/detalles-venta/{detalle.pk}/editar/',
            {'venta': venta.pk, 'producto': producto.pk, 'cantidad': 3, 'precio_unitario': '18.00'},
        )
        self.assertEqual(DetalleVenta.objects.get(pk=detalle.pk).cantidad, 3)
        self.client.post(f'/detalles-venta/{detalle.pk}/eliminar/')
        self.assertFalse(DetalleVenta.objects.filter(pk=detalle.pk).exists())
