from django.shortcuts import render, get_object_or_404, redirect
from .models import Lavanderia, TarifaVehiculo
from django.views.decorators.http import require_GET
from django.http import HttpResponseServerError, HttpResponseBadRequest ,JsonResponse
from .forms import LavanderiaForm, ConductorForm, VehiculoForm
from django.views.decorators.csrf import csrf_exempt
import requests
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
    tarifas_vehiculo = TarifaVehiculo.objects.all()

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

            # Verifica que tarifa_vehiculo y tiempo están presentes y asignados correctamente
            if 'tarifa_vehiculo' in request.POST and 'tiempo' in request.POST:
                tarifa_vehiculo_id = request.POST.get('tarifa_vehiculo')
                tiempo = request.POST.get('tiempo')
                try:
                    tarifa_vehiculo = TarifaVehiculo.objects.get(
                        id=tarifa_vehiculo_id)
                    lavanderia.tarifa_vehiculo = tarifa_vehiculo

                    # Asignar el precio basado en el tiempo del día seleccionado
                    if tiempo == 'manana':
                        lavanderia.precio = tarifa_vehiculo.precio_manana
                    elif tiempo == 'tarde':
                        lavanderia.precio = tarifa_vehiculo.precio_tarde
                    elif tiempo == 'noche':
                        lavanderia.precio = tarifa_vehiculo.precio_noche
                    elif tiempo == 'dia_completo':
                        lavanderia.precio = tarifa_vehiculo.precio_dia_completo
                    lavanderia.tiempo = tiempo

                    lavanderia.save()
                    # Cambia 'url_de_exito' por la URL de éxito correspondiente
                    return redirect('registro_lavanderia')
                except TarifaVehiculo.DoesNotExist:
                    return render(request, 'registro_lavanderia', {
                        'lavanderia_form': lavanderia_form,
                        'conductor_form': conductor_form,
                        'vehiculo_form': vehiculo_form,
                        'tarifas_vehiculo': tarifas_vehiculo,
                        'error_message': 'Tarifa de vehículo no encontrada'
                    })
            else:
                return render(request, 'registro_lavanderia', {
                    'lavanderia_form': lavanderia_form,
                    'conductor_form': conductor_form,
                    'vehiculo_form': vehiculo_form,
                    'tarifas_vehiculo': tarifas_vehiculo,
                    'error_message': 'Debe seleccionar una tarifa y un tiempo para el vehículo'
                })
    else:
        lavanderia_form = LavanderiaForm()
        conductor_form = ConductorForm()
        vehiculo_form = VehiculoForm()

    return render(request, 'lavanderia/registrarLavanderia.html', {
        'lavanderia_form': lavanderia_form,
        'conductor_form': conductor_form,
        'vehiculo_form': vehiculo_form,
        'tarifas_vehiculo': tarifas_vehiculo
    })


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


def salidas(request):
    if request.method == 'GET':
        # Obtener el número de DNI del formulario de búsqueda
        numero_dni = request.GET.get('numero_dni', '')

        if not numero_dni:
            # Si no se ingresó ningún número de DNI, renderizar nuevamente el formulario con un mensaje de error
            return render(request, 'salidas/salidas.html', {'error': 'Ingrese un número de DNI para realizar la búsqueda'})

        # Realizar la búsqueda en base al número de DNI
        resultados = Lavanderia.objects.filter(conductor__dni=numero_dni)

        # Renderizar la plantilla con los resultados de la búsqueda
        return render(request, 'salidas/salidas.html', {'resultados': resultados})

    # Manejar el caso en que el método de la solicitud no sea GET
    return HttpResponseBadRequest("Método no permitido")


def acceder_salida(request):
    lavanderia_id = request.GET.get('lavanderia_id')
    lavanderia = get_object_or_404(Lavanderia, id=lavanderia_id)
    # Aquí puedes agregar cualquier lógica adicional que necesites antes de renderizar la plantilla
    return render(request, 'salidas/accedersalida.html', {'lavanderia': lavanderia})
