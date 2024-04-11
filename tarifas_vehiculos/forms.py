# tarifas_vehiculos/forms.py

from django import forms
from .models import TarifaVehiculo


class TarifaVehiculoForm(forms.ModelForm):
    class Meta:
        model = TarifaVehiculo
        fields = '__all__'


class BusquedaTarifaForm(forms.Form):
    q = forms.CharField(label='Buscar por tipo de vehículo', max_length=100)
