from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APIClient

from .models import EvaluacionUbicacion, Farmacia, Zona
from .serializers import EvaluacionUbicacionSerializer, FarmaciaSerializer


class InvestigacionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.datos_zona = dict(nombre_zona='Zona LAB08', distrito='Lima',
                               densidad_poblacional=100, flujo_personas='Alto',
                               accesibilidad='Buena')
        self.zona = Zona.objects.create(**self.datos_zona)
        self.datos = dict(nombre='Botica LAB08', tipo='Independiente', zona=self.zona.pk,
                          distancia_metros=100, estado='Activa')

    def test_zona_crud_y_persistencia(self):
        base = '/api/v1/zonas/'
        self.assertEqual(self.client.get(base).status_code, 200)
        creado = self.client.post(base, self.datos_zona, format='json')
        self.assertEqual(creado.status_code, 201)
        url = f'{base}{creado.data["id"]}/'
        self.assertEqual(self.client.patch(url, {'distrito': 'Callao'}, format='json').status_code, 200)
        self.assertEqual(Zona.objects.get(pk=creado.data['id']).distrito, 'Callao')
        self.assertEqual(self.client.post(base, {}, format='json').status_code, 400)
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_farmacia_crud_y_validacion_distancia(self):
        base = '/api/v1/farmacias/'
        creado = self.client.post(base, self.datos, format='json')
        self.assertEqual(creado.status_code, 201)
        url = f'{base}{creado.data["id"]}/'
        self.assertEqual(self.client.get(url).status_code, 200)
        for distancia in [0, -1]:
            respuesta = self.client.post(base, {**self.datos, 'distancia_metros': distancia}, format='json')
            self.assertEqual(respuesta.status_code, 400)
            self.assertIn('distancia_metros', respuesta.data)
        self.assertEqual(self.client.patch(url, {'distancia_metros': 250}, format='json').status_code, 200)
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertFalse(Farmacia.objects.filter(pk=creado.data['id']).exists())
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_accion_activa_combina_busqueda_estado_y_orden(self):
        for nombre, estado, distancia in [('Botica B', 'Activa', 200), ('Botica A', 'ACTIVA', 100),
                                           ('Botica cerrada', 'Inactiva', 50), ('Otra', 'Activa', 80)]:
            Farmacia.objects.create(nombre=nombre, estado=estado, distancia_metros=distancia,
                                    tipo='Local', zona=self.zona)
        response = self.client.get('/api/v1/farmacias/activas/?search=Botica&ordering=distancia_metros')
        self.assertEqual([x['nombre'] for x in response.data], ['Botica A', 'Botica B'])
        self.assertEqual(self.client.get('/api/v1/farmacias/activas/?estado=Inactiva').data, [])
        self.assertEqual(Farmacia.objects.activas().count(), 3)

    def test_evaluacion_anidada_consultas_y_metodos_no_permitidos(self):
        for _ in range(3):
            EvaluacionUbicacion.objects.create(zona=self.zona, inkafarmas_cercanos=1,
                competidores_cercanos=2, centros_salud_cercanos=3, costo_alquiler='1000',
                ventas_estimadas='5000', nivel_viabilidad='Alta')
        with CaptureQueriesContext(connection) as antes:
            datos = EvaluacionUbicacionSerializer(EvaluacionUbicacion.objects.all(), many=True).data
        with CaptureQueriesContext(connection) as despues:
            optimizados = EvaluacionUbicacionSerializer(
                EvaluacionUbicacion.objects.select_related('zona'), many=True).data
        self.assertEqual(datos, optimizados)
        self.assertEqual(len(antes), 4)
        self.assertEqual(len(despues), 1)
        base = '/api/v1/evaluaciones/'
        self.assertEqual(self.client.get(base).data[0]['zona']['nombre_zona'], 'Zona LAB08')
        url = f'{base}{datos[0]["id"]}/'
        self.assertEqual(self.client.post(base, {}, format='json').status_code, 405)
        self.assertEqual(self.client.patch(url, {}, format='json').status_code, 405)
        self.assertEqual(self.client.delete(url).status_code, 405)

    def test_html_admin_y_api_coexisten(self):
        for url in ['/', '/productos/', '/zonas/', '/evaluaciones/', '/api/v1/']:
            self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(self.client.get('/admin/').status_code, 302)

    def test_serializer_farmacia_valida_y_no_persiste_invalido(self):
        valido = FarmaciaSerializer(data=self.datos)
        self.assertTrue(valido.is_valid(), valido.errors)
        objeto = valido.save()
        invalido = FarmaciaSerializer(objeto, data={'distancia_metros': 0}, partial=True)
        self.assertFalse(invalido.is_valid())
        objeto.refresh_from_db()
        self.assertEqual(objeto.distancia_metros, 100)
