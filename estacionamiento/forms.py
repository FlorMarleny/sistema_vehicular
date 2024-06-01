from django import forms
from .models import Cochera, Conductor, Vehiculo
from lavado.models import Lavanderia

class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = ['dni', 'nombres', 'apellidos', 'telefono', 'correo']

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'modelo', 'marca', 'matricula', 'color', 'serie', 'propietario']

class CocheraForm(forms.ModelForm):
    class Meta:
        model = Cochera
        fields = ['tarifa_vehiculo', 'tiempo']

class LavanderiaForm(forms.ModelForm):
    class Meta:
        model = Lavanderia
        fields = ['tarifa_vehiculo']

class ServicioForm(forms.Form):
    cochera = forms.BooleanField(required=False)
    lavanderia = forms.BooleanField(required=False)
