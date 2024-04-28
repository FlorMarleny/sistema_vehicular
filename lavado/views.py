from .forms import LavanderiaForm, ConductorForm, VehiculoForm
from .models import Lavanderia, Conductor, Vehiculo
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .forms import LavanderiaForm
from .models import Lavanderia
from django.shortcuts import render
import requests
from django.http import JsonResponse
from tarifas_vehiculos.models import TarifaVehiculo


def lavado_view(request):
    if request.method == 'POST':
        form = LavanderiaForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
    else:
        form = LavanderiaForm()

    tipos_vehiculo = TarifaVehiculo.objects.values_list(
        'tipo_vehiculo', flat=True).distinct()
    print("Tipos de vehículo:", tipos_vehiculo)

    return render(request, 'lavanderia/registrarLavanderia.html', {'form': form, 'tipos_vehiculo': tipos_vehiculo})


def historial_lavanderia(request):
    lavanderias = Lavanderia.objects.all()
    return render(request, 'lavanderia/historialLavanderia.html', {'lavanderias': lavanderias})


@csrf_exempt
def obtener_nombres_apellidos_por_dni(request):
    if request.method == 'POST':
        numero_dni = request.POST.get('dni')
        token = "apis-token-8038.WNWC8hV6ZnDUe2Ku3YF1Z8xVmBo1xscp"
        url = f"https://api.apis.net.pe/v2/reniec/dni?numero={numero_dni}"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            nombres = data.get('nombres')
            apellidos = f"{data.get('apellidoPaterno')} {data.get('apellidoMaterno')}"
            return JsonResponse({'nombres': nombres, 'apellidos': apellidos})
        else:
            return JsonResponse({'error': 'Error al obtener nombres y apellidos del DNI'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def registro_lavanderia(request):
    tipos_vehiculo = TarifaVehiculo.objects.values_list(
        'tipo_vehiculo', flat=True).distinct()

    if request.method == 'POST':
        lavanderia_form = LavanderiaForm(request.POST)
        conductor_form = ConductorForm(request.POST)
        vehiculo_form = VehiculoForm(request.POST)
        if lavanderia_form.is_valid() and conductor_form.is_valid() and vehiculo_form.is_valid():
            # Guardar los datos del conductor
            conductor = conductor_form.save()
            # Guardar los datos del vehículo
            vehiculo = vehiculo_form.save()
            # Guardar los datos de la lavandería
            lavanderia = lavanderia_form.save(commit=False)
            lavanderia.conductor = conductor
            lavanderia.vehiculo = vehiculo
            lavanderia.save()
            # Redirigir a la página de éxito
            # Ajusta según sea necesario
            return redirect('lavanderia/registrarLavanderia.html')
    else:
        lavanderia_form = LavanderiaForm()
        conductor_form = ConductorForm()
        vehiculo_form = VehiculoForm()

    return render(request, 'lavanderia/registrarLavanderia.html', {
        'lavanderia_form': lavanderia_form,
        'conductor_form': conductor_form,
        'vehiculo_form': vehiculo_form,
        'tipos_vehiculo': tipos_vehiculo
    })


def obtener_precio(request):
    if request.method == 'POST':
        tipo_vehiculo = request.POST.get('tipo_vehiculo')
        tiempo = request.POST.get('tiempo')

        if tiempo == 'manana':
            precio = TarifaVehiculo.objects.filter(
                tipo_vehiculo=tipo_vehiculo).values_list('precio_manana', flat=True).first()
        elif tiempo == 'tarde':
            precio = TarifaVehiculo.objects.filter(
                tipo_vehiculo=tipo_vehiculo).values_list('precio_tarde', flat=True).first()
        elif tiempo == 'noche':
            precio = TarifaVehiculo.objects.filter(
                tipo_vehiculo=tipo_vehiculo).values_list('precio_noche', flat=True).first()
        elif tiempo == 'dia_completo':
            precio = TarifaVehiculo.objects.filter(
                tipo_vehiculo=tipo_vehiculo).values_list('precio_dia_completo', flat=True).first()
        else:
            return JsonResponse({'error': 'Tiempo no válido'}, status=400)

        return JsonResponse({'precio': precio})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
