from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Cliente, DetalleVenta, PerfilCliente, Producto, Venta


class FarmaciaAdminTests(TestCase):
    def setUp(self):
        usuario = get_user_model().objects.create_superuser(
            username='admin_prueba', email='prueba@example.com', password='solo-test'
        )
        self.client.force_login(usuario)
        self.categoria = Categoria.objects.create(nombre='Vitaminas')
        self.producto = Producto.objects.create(
            nombre='Vitamina C', precio='12.50', stock=10, categoria=self.categoria
        )

    def test_busqueda_filtros_y_columnas(self):
        otra = Categoria.objects.create(nombre='Otros')
        Producto.objects.create(nombre='Jabon', precio='5', stock=3, categoria=otra)
        url = reverse('admin:farmacia_producto_changelist')
        respuesta = self.client.get(url, {'q': 'Vitamina'})
        self.assertContains(respuesta, 'Vitamina C')
        self.assertNotContains(respuesta, '>Jabon<')
        self.assertContains(respuesta, 'column-precio')
        respuesta = self.client.get(url, {'categoria__id__exact': self.categoria.pk})
        self.assertEqual(list(respuesta.context['cl'].queryset), [self.producto])

    def test_perfil_crear_editar_eliminar_desde_cliente(self):
        datos = {
            'nombre': 'Cliente de prueba', 'documento': 'LAB05',
            'telefono': '', 'correo': '',
            'perfil-TOTAL_FORMS': '1', 'perfil-INITIAL_FORMS': '0',
            'perfil-MIN_NUM_FORMS': '0', 'perfil-MAX_NUM_FORMS': '1',
            'perfil-0-direccion': 'Av. Prueba 123',
            'perfil-0-observaciones': 'Registro de prueba', '_save': 'Guardar',
        }
        respuesta = self.client.post(reverse('admin:farmacia_cliente_add'), datos)
        self.assertEqual(respuesta.status_code, 302)
        cliente = Cliente.objects.get(documento='LAB05')
        perfil = PerfilCliente.objects.get(cliente=cliente)
        url = reverse('admin:farmacia_cliente_change', args=[cliente.pk])
        datos.update({'perfil-INITIAL_FORMS': '1', 'perfil-0-id': str(perfil.pk),
                      'perfil-0-cliente': str(cliente.pk),
                      'perfil-0-direccion': 'Direccion actualizada'})
        self.assertEqual(self.client.post(url, datos).status_code, 302)
        perfil.refresh_from_db()
        self.assertEqual(perfil.direccion, 'Direccion actualizada')
        datos['perfil-0-DELETE'] = 'on'
        self.assertEqual(self.client.post(url, datos).status_code, 302)
        self.assertFalse(PerfilCliente.objects.filter(pk=perfil.pk).exists())
        self.assertTrue(Cliente.objects.filter(pk=cliente.pk).exists())

    def test_detalle_crear_editar_eliminar_desde_venta(self):
        cliente = Cliente.objects.create(nombre='Cliente venta', documento='VENTA05')
        datos = {
            'cliente': str(cliente.pk), 'fecha_0': '2026-09-19', 'fecha_1': '12:00:00',
            'total': '25.00', 'detalles-TOTAL_FORMS': '1',
            'detalles-INITIAL_FORMS': '0', 'detalles-MIN_NUM_FORMS': '0',
            'detalles-MAX_NUM_FORMS': '1000',
            'detalles-0-producto': str(self.producto.pk),
            'detalles-0-cantidad': '2', 'detalles-0-precio_unitario': '12.50',
            '_save': 'Guardar',
        }
        respuesta = self.client.post(reverse('admin:farmacia_venta_add'), datos)
        self.assertEqual(respuesta.status_code, 302)
        venta = Venta.objects.get(cliente=cliente)
        detalle = DetalleVenta.objects.get(venta=venta)
        self.assertEqual(list(venta.productos.all()), [self.producto])
        url = reverse('admin:farmacia_venta_change', args=[venta.pk])
        datos.update({'detalles-INITIAL_FORMS': '1', 'detalles-0-id': str(detalle.pk),
                      'detalles-0-venta': str(venta.pk), 'detalles-0-cantidad': '3',
                      'total': '37.50'})
        self.assertEqual(self.client.post(url, datos).status_code, 302)
        detalle.refresh_from_db()
        self.assertEqual(detalle.subtotal, Decimal('37.50'))
        datos['detalles-0-DELETE'] = 'on'
        datos['total'] = '0.00'
        self.assertEqual(self.client.post(url, datos).status_code, 302)
        self.assertFalse(DetalleVenta.objects.filter(pk=detalle.pk).exists())
        self.assertTrue(Venta.objects.filter(pk=venta.pk).exists())

    def test_producto_crear_editar_eliminar_con_categoria(self):
        datos = {'nombre': 'Producto temporal', 'descripcion': '', 'precio': '8.00',
                 'stock': '4', 'categoria': str(self.categoria.pk), '_save': 'Guardar'}
        self.assertEqual(self.client.post(reverse('admin:farmacia_producto_add'), datos).status_code, 302)
        producto = Producto.objects.get(nombre='Producto temporal')
        datos['stock'] = '7'
        url = reverse('admin:farmacia_producto_change', args=[producto.pk])
        self.assertEqual(self.client.post(url, datos).status_code, 302)
        producto.refresh_from_db()
        self.assertEqual(producto.stock, 7)
        self.assertEqual(producto.categoria, self.categoria)
        url = reverse('admin:farmacia_producto_delete', args=[producto.pk])
        self.assertEqual(self.client.post(url, {'post': 'yes'}).status_code, 302)
        self.assertFalse(Producto.objects.filter(pk=producto.pk).exists())

    def test_admin_exige_autenticacion(self):
        self.client.logout()
        respuesta = self.client.get(reverse('admin:farmacia_cliente_changelist'))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/admin/login/', respuesta.url)
