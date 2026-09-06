from django import forms

from .models import Categoria, Cliente, Producto, Proveedor, Venta


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


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


class VentaForm(BaseModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'fecha', 'total']
        widgets = {'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}), 'total': forms.NumberInput(attrs={'step': '0.01', 'min': '0'})}
