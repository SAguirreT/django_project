from django import forms
from .models import Zona, Farmacia, EvaluacionUbicacion


class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = [
            'nombre_zona',
            'distrito',
            'densidad_poblacional',
            'flujo_personas',
            'accesibilidad',
        ]


class FarmaciaForm(forms.ModelForm):
    class Meta:
        model = Farmacia
        fields = [
            'nombre',
            'tipo',
            'zona',
            'distancia_metros',
            'estado',
        ]


class EvaluacionUbicacionForm(forms.ModelForm):
    class Meta:
        model = EvaluacionUbicacion
        fields = [
            'zona',
            'inkafarmas_cercanos',
            'competidores_cercanos',
            'centros_salud_cercanos',
            'costo_alquiler',
            'ventas_estimadas',
            'nivel_viabilidad',
        ]