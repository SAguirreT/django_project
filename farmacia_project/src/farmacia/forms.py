from django import forms

from .models import (
    Categoria, Cliente, DetalleVenta, EvaluacionUbicacion, Farmacia,
    PerfilCliente, Producto, Proveedor, Venta, Zona,
)


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): field.widget.attrs['class'] = 'form-control'


class ZonaForm(BaseModelForm):
    class Meta:
        model = Zona
        fields = ['nombre_zona', 'distrito', 'densidad_poblacional', 'flujo_personas', 'accesibilidad']


class FarmaciaForm(BaseModelForm):
    class Meta:
        model = Farmacia
        fields = ['nombre', 'tipo', 'zona', 'distancia_metros', 'estado']


class EvaluacionUbicacionForm(BaseModelForm):
    class Meta:
        model = EvaluacionUbicacion
        fields = ['zona', 'inkafarmas_cercanos', 'competidores_cercanos', 'centros_salud_cercanos', 'costo_alquiler', 'ventas_estimadas', 'nivel_viabilidad']


class CategoriaForm(BaseModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}


class ProductoForm(BaseModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3}), 'precio': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}), 'stock': forms.NumberInput(attrs={'min': '0'})}


class ProveedorForm(BaseModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'correo', 'direccion']


class ClienteForm(BaseModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'documento', 'telefono', 'correo']


class PerfilClienteForm(BaseModelForm):
    class Meta:
        model = PerfilCliente
        fields = ['cliente', 'direccion', 'observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'rows': 3})}


class VentaForm(BaseModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'fecha', 'total']
        widgets = {'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}), 'total': forms.NumberInput(attrs={'step': '0.01', 'min': '0'})}


class DetalleVentaForm(BaseModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['venta', 'producto', 'cantidad', 'precio_unitario']
        widgets = {'cantidad': forms.NumberInput(attrs={'min': '1'}), 'precio_unitario': forms.NumberInput(attrs={'step': '0.01', 'min': '0'})}
