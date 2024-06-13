from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Usuario o contraseña incorrectos.'
            return render(request, 'registration/login.html', {'error_message': error_message})
    else:
        return render(request, 'registration/login.html')
    
    

from lavado.models import Lavanderia
from tarifas_vehiculos.models import TarifaVehiculo

from datetime import date
from django.db.models import Sum

from django.db.models import Count

@login_required
def dashboard_view(request):
    
    # Contar vehículos ingresados en lavado (estado 'en_proceso' y lavadero=True)
    vehiculos_ingresados_lavado = Lavanderia.objects.filter(estado='en_proceso', lavadero=True).count()

    # Contar vehículos ingresados en cochera (estado 'en_proceso' y cochera=True)
    vehiculos_ingresados_cochera = Lavanderia.objects.filter(estado='en_proceso', cochera=True).count()

    # Contar vehículos salidos de lavado (estado 'terminada' y lavadero=True)
    vehiculos_salidos_lavado = Lavanderia.objects.filter(estado='terminada', lavadero=True).count()

    # Contar vehículos salidos de cochera (estado 'terminada' y cochera=True)
    vehiculos_salidos_cochera = Lavanderia.objects.filter(estado='terminada', cochera=True).count()

    vehiculos_por_tipo = TarifaVehiculo.objects.values('tipo_vehiculo').annotate(count=Count('tipo_vehiculo'))


    return render(request, 'dashboard.html', {
        'vehiculos_por_tipo': vehiculos_por_tipo,
        'vehiculos_ingresados_lavado': vehiculos_ingresados_lavado,
        'vehiculos_ingresados_cochera': vehiculos_ingresados_cochera,
        'vehiculos_salidos_lavado': vehiculos_salidos_lavado,
        'vehiculos_salidos_cochera': vehiculos_salidos_cochera,
    })


def logout_view(request):
    return render(request, 'registration/login.html')
