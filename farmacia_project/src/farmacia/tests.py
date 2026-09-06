from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from .models import Categoria, Cliente, Producto, Proveedor, Venta


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
