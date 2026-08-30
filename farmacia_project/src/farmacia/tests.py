from django.test import SimpleTestCase

from farmacia.forms import EvaluacionUbicacionForm, FarmaciaForm, ZonaForm
from farmacia.models import calculate_viability, evaluaciones, farmacias, zonas


class FarmaciaProjectTests(SimpleTestCase):
    def test_zonas_seed_data_exists(self):
        self.assertGreater(len(zonas), 4)

    def test_farmacias_seed_data_exists(self):
        self.assertGreater(len(farmacias), 4)

    def test_evaluaciones_seed_data_exists(self):
        self.assertGreater(len(evaluaciones), 4)

    def test_zone_form_validates_required_fields(self):
        form = ZonaForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('nombre_zona', form.errors)

    def test_farmacia_form_validates_distance(self):
        form = FarmaciaForm(data={
            'nombre': 'Botica San Martín',
            'tipo': 'Inkafarma',
            'zona_id': '1',
            'distancia_metros': -10,
            'estado': 'Activa',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('distancia_metros', form.errors)

    def test_evaluacion_form_validates_non_negative_fields(self):
        form = EvaluacionUbicacionForm(data={
            'zona_id': '1',
            'inkafarmas_cercanos': -1,
            'competidores_cercanos': 2,
            'centros_salud_cercanos': 1,
            'costo_alquiler': 1500,
            'ventas_estimadas': 20000,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('inkafarmas_cercanos', form.errors)

    def test_calculate_viability_returns_known_level(self):
        result = calculate_viability(
            densidad_poblacional=9000,
            flujo_personas='Alto',
            accesibilidad='Alta',
            inkafarmas_cercanos=1,
            competidores_cercanos=1,
            centros_salud_cercanos=2,
            costo_alquiler=1800,
            ventas_estimadas=45000,
        )
        self.assertIn(result, ['Baja', 'Media', 'Alta'])
