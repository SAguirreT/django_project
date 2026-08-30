from django import forms

from .models import zonas

FLUJO_CHOICES = [
    ('Bajo', 'Bajo'),
    ('Medio', 'Medio'),
    ('Alto', 'Alto'),
]

ACCESIBILIDAD_CHOICES = [
    ('Baja', 'Baja'),
    ('Media', 'Media'),
    ('Alta', 'Alta'),
]

TIPO_CHOICES = [
    ('Inkafarma', 'Inkafarma'),
    ('Competencia', 'Competencia'),
]

ESTADO_CHOICES = [
    ('Activa', 'Activa'),
    ('Cerrada', 'Cerrada'),
]

ZONA_CHOICES = [(zona['id'], zona['nombre_zona']) for zona in zonas]


class ZonaForm(forms.Form):
    nombre_zona = forms.CharField(max_length=100, label='Nombre de la zona')
    distrito = forms.CharField(max_length=100, label='Distrito')
    densidad_poblacional = forms.IntegerField(min_value=1, label='Densidad poblacional')
    flujo_personas = forms.ChoiceField(choices=FLUJO_CHOICES, label='Flujo de personas')
    accesibilidad = forms.ChoiceField(choices=ACCESIBILIDAD_CHOICES, label='Accesibilidad')

    def clean_nombre_zona(self):
        nombre = self.cleaned_data['nombre_zona']
        if not nombre.strip():
            raise forms.ValidationError('El nombre es obligatorio.')
        return nombre.strip()

    def clean_distrito(self):
        distrito = self.cleaned_data['distrito']
        if not distrito.strip():
            raise forms.ValidationError('El distrito es obligatorio.')
        return distrito.strip()


class FarmaciaForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre de la farmacia')
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, label='Tipo')
    zona_id = forms.ChoiceField(choices=ZONA_CHOICES, label='Zona')
    distancia_metros = forms.IntegerField(min_value=0, label='Distancia (m)')
    estado = forms.ChoiceField(choices=ESTADO_CHOICES, label='Estado')

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not nombre.strip():
            raise forms.ValidationError('El nombre es obligatorio.')
        return nombre.strip()

    def clean_zona_id(self):
        zona_id = self.cleaned_data['zona_id']
        if not any(zona['id'] == int(zona_id) for zona in zonas):
            raise forms.ValidationError('La zona seleccionada no es válida.')
        return int(zona_id)


class EvaluacionUbicacionForm(forms.Form):
    zona_id = forms.ChoiceField(choices=ZONA_CHOICES, label='Zona')
    inkafarmas_cercanos = forms.IntegerField(min_value=0, label='Inkafarmas cercanos')
    competidores_cercanos = forms.IntegerField(min_value=0, label='Competidores cercanos')
    centros_salud_cercanos = forms.IntegerField(min_value=0, label='Centros de salud cercanos')
    costo_alquiler = forms.DecimalField(min_value=0.01, max_digits=12, decimal_places=2, label='Costo de alquiler')
    ventas_estimadas = forms.DecimalField(min_value=0, max_digits=12, decimal_places=2, label='Ventas estimadas')

    def clean_zona_id(self):
        zona_id = self.cleaned_data['zona_id']
        if not any(zona['id'] == int(zona_id) for zona in zonas):
            raise forms.ValidationError('La zona seleccionada no es válida.')
        return int(zona_id)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('costo_alquiler') is not None and cleaned_data['costo_alquiler'] <= 0:
            self.add_error('costo_alquiler', 'El costo de alquiler debe ser mayor que 0.')
        if cleaned_data.get('ventas_estimadas') is not None and cleaned_data['ventas_estimadas'] < 0:
            self.add_error('ventas_estimadas', 'Las ventas estimadas no pueden ser negativas.')
        return cleaned_data
