from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from .models import Categoria, Cliente, DetalleVenta, PerfilCliente, Producto, Venta


class TemplateRefactorTests(TestCase):
    def test_clientes_list_uses_base_and_default_profile_value(self):
        cliente = Cliente.objects.create(nombre='Ana Torres', documento='12345678')
        categoria = Categoria.objects.create(nombre='Vitaminas')
        producto = Producto.objects.create(nombre='Vitamina C', precio=Decimal('20.00'), stock=10, categoria=categoria)
        venta = Venta.objects.create(cliente=cliente, fecha=timezone.now(), total=Decimal('20.00'))
        venta.productos.add(producto, through_defaults={'cantidad': 1, 'precio_unitario': Decimal('20.00')})

        response = self.client.get('/clientes/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, '-')
        self.assertContains(response, 'Ana Torres')

    def test_categoria_list_displays_all_products(self):
        categoria = Categoria.objects.create(nombre='Analgesicos', descripcion='Para dolor')
        Producto.objects.create(nombre='Ibuprofeno', precio=Decimal('10.00'), stock=5, categoria=categoria)
        Producto.objects.create(nombre='Paracetamol', precio=Decimal('8.50'), stock=7, categoria=categoria)

        response = self.client.get('/categorias/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ibuprofeno')
        self.assertContains(response, 'Paracetamol')
        self.assertContains(response, '2')

    def test_venta_detail_shows_product_data_with_two_decimals(self):
        cliente = Cliente.objects.create(nombre='Luis Ramos', documento='87654321')
        categoria = Categoria.objects.create(nombre='Antigripales')
        producto = Producto.objects.create(nombre='Jarabe', precio=Decimal('18.00'), stock=8, categoria=categoria)
        venta = Venta.objects.create(cliente=cliente, fecha=timezone.now(), total=Decimal('36.00'))
        DetalleVenta.objects.create(venta=venta, producto=producto, cantidad=2, precio_unitario=Decimal('18.00'))

        response = self.client.get(f'/ventas/{venta.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jarabe')
        self.assertContains(response, '2')
        self.assertContains(response, '18,00')
        self.assertContains(response, '36,00')

    def test_xss_is_escaped_in_listings(self):
        categoria = Categoria.objects.create(nombre='<script>alert("xss")</script>')
        Producto.objects.create(nombre='Droga', precio=Decimal('12.00'), stock=5, categoria=categoria)

        response = self.client.get('/categorias/')

        self.assertContains(response, '&lt;SCRIPT&gt;ALERT(&quot;XSS&quot;)&lt;/SCRIPT&gt;')
        self.assertNotContains(response, '<script>alert("xss")</script>')

    def test_delete_pages_use_confirm_partial(self):
        categoria = Categoria.objects.create(nombre='Vitaminas')
        producto = Producto.objects.create(nombre='Vitamina C', precio=Decimal('20.00'), stock=10, categoria=categoria)
        cliente = Cliente.objects.create(nombre='Persona', documento='11111111')
        perfil = PerfilCliente.objects.create(cliente=cliente, direccion='Avenida 1')

        response_producto = self.client.get(f'/productos/{producto.pk}/eliminar/')
        response_perfil = self.client.get(f'/perfil/{perfil.pk}/eliminar/')

        self.assertTemplateUsed(response_producto, 'farmacia/partials/_confirm_delete.html')
        self.assertTemplateUsed(response_perfil, 'farmacia/partials/_confirm_delete.html')
