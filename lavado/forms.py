from django import forms
from .models import Lavanderia, Conductor, Vehiculo

class LavanderiaForm(forms.ModelForm):
    class Meta:
        model = Lavanderia
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

class ServicioForm(forms.Form):
    cochera = forms.BooleanField(required=False)
    lavanderia = forms.BooleanField(required=False)

