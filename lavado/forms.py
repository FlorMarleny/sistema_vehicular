# lavado/forms.py

from django import forms

class LavanderiaForm(forms.Form):
    # Define los campos de tu formulario aquí
    dni = forms.CharField(max_length=8)
