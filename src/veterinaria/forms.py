from django import forms
from .models import Propietario


class PropietarioForm(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = ['nombre', 'apellido', 'telefono', 'correo']