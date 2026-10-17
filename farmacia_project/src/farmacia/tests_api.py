from decimal import Decimal

from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from rest_framework.test import APIClient

from .models import Categoria, Cliente, DetalleVenta, Farmacia, Producto, Venta, Zona
from .serializers import ProductoSerializer, VentaReadSerializer


class FarmaciaApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.categoria = Categoria.objects.create(nombre='Categoría API')
        self.producto = Producto.objects.create(
            nombre='Producto API', descripcion='', precio=Decimal('4.50'),
            stock=3, categoria=self.categoria,
        )

    def test_producto_crud_http_y_validacion(self):
        listado = self.client.get('/api/v1/productos/')
        self.assertEqual(listado.status_code, 200)

        datos = {
            'nombre': 'Temporal API', 'descripcion': '', 'precio': '2.00',
            'stock': 1, 'categoria': self.categoria.pk,
        }
        creado = self.client.post('/api/v1/productos/', datos, format='json')
        self.assertEqual(creado.status_code, 201)
        pk = creado.data['id']

        invalido = self.client.post(
            '/api/v1/productos/', {**datos, 'precio': '0'}, format='json'
        )
        self.assertEqual(invalido.status_code, 400)
        self.assertEqual(self.client.get('/api/v1/productos/999999/').status_code, 404)
        self.assertEqual(self.client.patch(
            f'/api/v1/productos/{pk}/', {'stock': 2}, format='json'
        ).status_code, 200)
        self.assertEqual(self.client.delete(f'/api/v1/productos/{pk}/').status_code, 204)

    def test_categoria_crud_viewset_y_filtros(self):
        self.assertEqual(self.client.get('/api/v1/categorias/').status_code, 200)
        respuesta = self.client.post(
            '/api/v1/categorias/', {'nombre': 'Temporal', 'descripcion': ''}, format='json'
        )
        self.assertEqual(respuesta.status_code, 201)
        self.assertContains(self.client.get('/api/v1/productos/?search=Producto'), 'Producto API')
        self.assertEqual(self.client.get('/api/v1/productos/?disponible=true').status_code, 200)
        self.assertEqual(self.client.get('/api/v1/productos/con-stock/').status_code, 200)

    def test_model_serializer_objeto_lista_validacion_y_save(self):
        uno = ProductoSerializer(self.producto)
        varios = ProductoSerializer(Producto.objects.all(), many=True)
        self.assertEqual(uno.data['nombre'], 'Producto API')
        self.assertEqual(len(varios.data), 1)

        valido = ProductoSerializer(data={
            'nombre': 'Guardado por serializer', 'descripcion': '',
            'precio': '3.25', 'stock': 1, 'categoria': self.categoria.pk,
        })
        self.assertTrue(valido.is_valid(), valido.errors)
        self.assertEqual(valido.validated_data['precio'], Decimal('3.25'))
        guardado = valido.save()
        self.assertEqual(guardado.nombre, 'Guardado por serializer')

        invalido = ProductoSerializer(data={
            'nombre': 'Precio inválido', 'descripcion': '', 'precio': '0',
            'stock': 1, 'categoria': self.categoria.pk,
        })
        self.assertFalse(invalido.is_valid())
        self.assertIn('precio', invalido.errors)

    def test_vistas_genericas_list_create_y_detalle(self):
        lista = '/api/v1/basico/productos/'
        detalle = f'{lista}{self.producto.pk}/'
        self.assertEqual(self.client.get(lista).status_code, 200)
        self.assertEqual(self.client.get(detalle).status_code, 200)
        creado = self.client.post(lista, {
            'nombre': 'Genérico', 'descripcion': '', 'precio': '1.00',
            'stock': 1, 'categoria': self.categoria.pk,
        }, format='json')
        self.assertEqual(creado.status_code, 201)

    def test_venta_anidada_solo_lectura_y_consultas_optimizadas(self):
        cliente = Cliente.objects.create(nombre='Cliente API', documento='API-001')
        venta = Venta.objects.create(cliente=cliente, fecha=timezone.now(), total='9.00')
        DetalleVenta.objects.create(
            venta=venta, producto=self.producto, cantidad=2, precio_unitario='4.50'
        )

        url = '/api/v1/ventas/'
        response = self.client.get(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        results = response.data['results'] if isinstance(response.data, dict) else response.data
        self.assertEqual(results[0]['detalles'][0]['producto']['nombre'], 'Producto API')
        self.assertEqual(self.client.post(url, {}, format='json').status_code, 405)

        with self.assertNumQueries(4):
            self.client.get(url, HTTP_ACCEPT='application/json')

        with CaptureQueriesContext(connection) as before:
            VentaReadSerializer(Venta.objects.all(), many=True).data
        with CaptureQueriesContext(connection) as after:
            optimized = Venta.objects.select_related('cliente').prefetch_related(
                'detalles__producto__categoria'
            )
            VentaReadSerializer(optimized, many=True).data
        self.assertEqual(len(before), 5)
        self.assertEqual(len(after), 4)

    def test_filtro_estado_de_farmacia(self):
        zona = Zona.objects.create(
            nombre_zona='Zona API', distrito='Centro', densidad_poblacional=100,
            flujo_personas='Alto', accesibilidad='Buena',
        )
        Farmacia.objects.create(
            nombre='Farmacia Activa', tipo='Cadena', zona=zona,
            distancia_metros=100, estado='Activa',
        )
        respuesta = self.client.get('/api/v1/farmacias/?estado=activa')
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Farmacia Activa')
