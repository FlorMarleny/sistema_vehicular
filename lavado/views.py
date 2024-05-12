from django.http import HttpResponseServerError
from .forms import LavanderiaForm, ConductorForm, VehiculoForm
from .models import Lavanderia, Conductor, Vehiculo
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from tarifas_vehiculos.models import TarifaVehiculo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


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


# def historial_lavanderia(request):
#     lavanderias = Lavanderia.objects.all()
#     return render(request, 'lavanderia/historialLavanderia.html', {'lavanderias': lavanderias})

# from django.shortcuts import render
# from .models import Lavanderia

def historial_lavanderia(request):
    query = request.GET.get('q')

    lavanderias = Lavanderia.objects.filter(lavadero=True)

    total_registros = lavanderias.count()

    if query:
        lavanderias = lavanderias.filter(
            Q(conductor__nombres__icontains=query) |
            Q(conductor__apellidos__icontains=query) |
            Q(vehiculo__placa__icontains=query) |
            Q(tipo_vehiculo__icontains=query)
        )

    paginator = Paginator(lavanderias, 10)

    page_number = request.GET.get('page')
    try:
        lavanderias = paginator.page(page_number)
    except PageNotAnInteger:
        lavanderias = paginator.page(1)
    except EmptyPage:
        lavanderias = paginator.page(paginator.num_pages)

    return render(request, 'lavanderia/historialLavanderia.html', {'lavanderias': lavanderias, 'total_registros': total_registros})


def historial_cochera(request):
    query = request.GET.get('q')

    lavanderias = Lavanderia.objects.filter(cochera=True)

    total_registros = lavanderias.count()

    if query:
        lavanderias = lavanderias.filter(
            Q(conductor__nombres__icontains=query) |
            Q(conductor__apellidos__icontains=query) |
            Q(vehiculo__placa__icontains=query) |
            Q(tipo_vehiculo__icontains=query)
        )

    paginator = Paginator(lavanderias, 10)

    page_number = request.GET.get('page')
    try:
        lavanderias = paginator.page(page_number)
    except PageNotAnInteger:
        lavanderias = paginator.page(1)
    except EmptyPage:
        lavanderias = paginator.page(paginator.num_pages)

    return render(request, 'cochera/historialCochera.html', {'lavanderias': lavanderias, 'total_registros': total_registros})


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
            conductor = conductor_form.save()
            vehiculo = vehiculo_form.save()
            lavanderia = lavanderia_form.save(commit=False)
            lavanderia.conductor = conductor
            lavanderia.vehiculo = vehiculo
            lavanderia.save()
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


def editar_lavanderia(request, id):
    lavanderia = get_object_or_404(Lavanderia, id=id)
    print("Lavanderia obtenida:", lavanderia)

    if request.method == 'POST':
        lavanderia_form = LavanderiaForm(request.POST, instance=lavanderia)
        conductor_form = ConductorForm(
            request.POST, instance=lavanderia.conductor)
        vehiculo_form = VehiculoForm(
            request.POST, instance=lavanderia.vehiculo)
        print("Datos POST recibidos:", request.POST)

        if lavanderia_form.is_valid() and conductor_form.is_valid() and vehiculo_form.is_valid():
            print("Todos los formularios son válidos")
            conductor = conductor_form.save()
            vehiculo = vehiculo_form.save()
            lavanderia = lavanderia_form.save(commit=False)
            lavanderia.conductor = conductor
            lavanderia.vehiculo = vehiculo
            lavanderia.save()

            print("Lavanderia guardada exitosamente")
            return redirect('historial_lavanderia')
        else:
            print("Errores de validación en al menos uno de los formularios:")
            print("LavanderiaForm:", lavanderia_form.errors)
            print("ConductorForm:", conductor_form.errors)
            print("VehiculoForm:", vehiculo_form.errors)
            return HttpResponseServerError("Error en el formulario. Revise los errores e inténtelo de nuevo.")
    else:
        lavanderia_form = LavanderiaForm(instance=lavanderia)
        conductor_form = ConductorForm(instance=lavanderia.conductor)
        vehiculo_form = VehiculoForm(instance=lavanderia.vehiculo)

    tipo_vehiculo = lavanderia.tipo_vehiculo if lavanderia else None

    return render(request, 'lavanderia/editar_lavanderia.html', {'lavanderia': lavanderia, 'lavanderia_form': lavanderia_form, 'conductor_form': conductor_form, 'vehiculo_form': vehiculo_form, 'tipo_vehiculo': tipo_vehiculo})


def detalles_lavanderia(request, id):
    lavanderia = get_object_or_404(Lavanderia, id=id)
    return render(request, 'lavanderia/detalles_lavanderia.html', {'lavanderia': lavanderia})


def eliminar_lavanderia(request, id):
    lavanderia = get_object_or_404(Lavanderia, id=id)
    return render(request, 'lavanderia/eliminar_lavanderia.html', {'lavanderia': lavanderia})
