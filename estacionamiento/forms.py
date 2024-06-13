from django import forms
from .models import Cochera
from lavado.models import Conductor, Vehiculo


class CocheraForm(forms.ModelForm):
    class Meta:
        model = Cochera
        fields = ['conductor', 'vehiculo', 'lavadero', 'cochera',
                  'tiempo', 'precio_cochera', 'tarifa_vehiculo']
        exclude = ['conductor', 'vehiculo']

class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = ['dni', 'nombres', 'apellidos', 'telefono', 'correo']

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'modelo', 'marca',
                  'matricula', 'color', 'serie', 'propietario']
