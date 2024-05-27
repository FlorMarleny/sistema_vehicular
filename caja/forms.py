from django import forms

class CerrarCajaLavanderiaForm(forms.Form):
    total_lavanderia = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
