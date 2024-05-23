from django.utils import timezone
from .models import Lavanderia, Lavanderia, TarifaVehiculo
from django.http import HttpResponseBadRequest , HttpResponseServerError, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import LavanderiaForm, ConductorForm, VehiculoForm
from django.views.decorators.csrf import csrf_exempt
import requests
from tarifas_vehiculos.models import TarifaVehiculo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse


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
            print("Todos los formularios son válidos.")
            conductor = conductor_form.save()
            vehiculo = vehiculo_form.save()
            lavanderia = lavanderia_form.save(commit=False)
            lavanderia.conductor = conductor
            lavanderia.vehiculo = vehiculo

            if 'tarifa_vehiculo' in request.POST and 'tiempo' in request.POST:
                tarifa_vehiculo_id = request.POST.get('tarifa_vehiculo')
                tiempo = request.POST.get('tiempo')
                try:
                    tarifa_vehiculo = TarifaVehiculo.objects.get( id=tarifa_vehiculo_id)
                    lavanderia.tarifa_vehiculo = tarifa_vehiculo

                    if tiempo == 'manana':
                        lavanderia.precio_cochera = tarifa_vehiculo.precio_manana
                    elif tiempo == 'tarde':
                        lavanderia.precio_cochera = tarifa_vehiculo.precio_tarde
                    elif tiempo == 'noche':
                        lavanderia.precio_cochera = tarifa_vehiculo.precio_noche
                    elif tiempo == 'dia_completo':
                        lavanderia.precio_cochera = tarifa_vehiculo.precio_dia_completo
                    lavanderia.tiempo = tiempo

                    lavanderia.total_a_pagar = lavanderia.calcular_total_a_pagar()
                    lavanderia.save()

                    print("Lavandería guardada correctamente.")
                    return redirect('registro_lavanderia')
                except TarifaVehiculo.DoesNotExist:
                    print("Tarifa de vehículo no encontrada.")
                    return render(request, 'lavanderia/registrarLavanderia.html', {
                        'lavanderia_form': lavanderia_form,
                        'conductor_form': conductor_form,
                        'vehiculo_form': vehiculo_form,
                        'tarifas_vehiculo': tarifas_vehiculo,
                        'error_message': 'Tarifa de vehículo no encontrada'
                    })
            else:
                print("Tarifa de vehículo o tiempo no seleccionados.")
                return render(request, 'lavanderia/registrarLavanderia.html', {
                    'lavanderia_form': lavanderia_form,
                    'conductor_form': conductor_form,
                    'vehiculo_form': vehiculo_form,
                    'tarifas_vehiculo': tarifas_vehiculo,
                    'error_message': 'Debe seleccionar una tarifa y un tiempo para el vehículo'
                })
        else:
            print("Errores en los formularios.")
            error_messages = []
            if not lavanderia_form.is_valid():
                error_messages.append('Error en el formulario de lavandería.')
                print(lavanderia_form.errors)
            if not conductor_form.is_valid():
                error_messages.append('Error en el formulario de conductor.')
                print(conductor_form.errors)
            if not vehiculo_form.is_valid():
                error_messages.append('Error en el formulario de vehículo.')
                print(vehiculo_form.errors)

            return render(request, 'lavanderia/registrarLavanderia.html', {
                'lavanderia_form': lavanderia_form,
                'conductor_form': conductor_form,
                'vehiculo_form': vehiculo_form,
                'tarifas_vehiculo': tarifas_vehiculo,
                'error_message': ' '.join(error_messages),
            })
    else:
        lavanderia_form = LavanderiaForm()
        conductor_form = ConductorForm()
        vehiculo_form = VehiculoForm()

    return render(request, 'lavanderia/registrarLavanderia.html', {
        'lavanderia_form': lavanderia_form,
        'conductor_form': conductor_form,
        'vehiculo_form': vehiculo_form,
        'tarifas_vehiculo': tarifas_vehiculo,
    })

def editar_lavanderia(request, id):
    lavanderia = get_object_or_404(Lavanderia, id=id)
    tarifas_vehiculo = TarifaVehiculo.objects.all()

    if request.method == 'POST':
        lavanderia_form = LavanderiaForm(request.POST, instance=lavanderia)
        conductor_form = ConductorForm(request.POST, instance=lavanderia.conductor)
        vehiculo_form = VehiculoForm(request.POST, instance=lavanderia.vehiculo)

        if lavanderia_form.is_valid() and conductor_form.is_valid() and vehiculo_form.is_valid():
            lavanderia = lavanderia_form.save(commit=False)
            conductor = conductor_form.save()
            vehiculo = vehiculo_form.save()

            if 'tarifa_vehiculo' in request.POST and 'tiempo' in request.POST:
                tarifa_vehiculo_id = request.POST.get('tarifa_vehiculo')
                tiempo = request.POST.get('tiempo')
                try:
                    tarifa_vehiculo = TarifaVehiculo.objects.get(id=tarifa_vehiculo_id)
                    lavanderia.tarifa_vehiculo = tarifa_vehiculo
                    lavanderia.tiempo = tiempo
                    
                    
                        
                    # Calcular el precio basado en la tarifa seleccionada y el tiempo
                    if tiempo == 'manana':
                        lavanderia.precio_cochera = tarifa_vehiculo.precio_manana
                    elif tiempo == 'tarde':
                        lavanderia.precio_cochera = tarifa_vehiculo.precio_tarde
                    elif tiempo == 'noche':
                        lavanderia.precio_cochera = tarifa_vehiculo.precio_noche
                    elif tiempo == 'dia_completo':
                        lavanderia.precio_cochera = tarifa_vehiculo.precio_dia_completo
                    
                    
                    lavanderia.total_a_pagar = lavanderia.calcular_total_a_pagar()
                    lavanderia.save()

                    return redirect('historial_lavanderia')
                except TarifaVehiculo.DoesNotExist:
                    # Manejar el caso donde la tarifa de vehículo no existe
                    pass
    else:
        lavanderia_form = LavanderiaForm(instance=lavanderia)
        conductor_form = ConductorForm(instance=lavanderia.conductor)
        vehiculo_form = VehiculoForm(instance=lavanderia.vehiculo)

    return render(request, 'lavanderia/editar_lavanderia.html', {
        'lavanderia': lavanderia,
        'lavanderia_form': lavanderia_form,
        'conductor_form': conductor_form,
        'vehiculo_form': vehiculo_form,
        'tarifas_vehiculo': tarifas_vehiculo,
    })


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
    if request.method == 'GET':
        lavanderia_id = request.GET.get('lavanderia_id')
        lavanderia = get_object_or_404(Lavanderia, id=lavanderia_id)
        
        return render(request, 'salidas/accedersalida.html', {'lavanderia': lavanderia})
    
    elif request.method == 'POST':
        lavanderia_id = request.POST.get('lavanderia_id')
        lavanderia = get_object_or_404(Lavanderia, id=lavanderia_id)
        efectivo = request.POST.get('efectivo')
        vuelto = request.POST.get('vuelto')
        
        try:
            lavanderia.efectivo = float(efectivo)
            lavanderia.vuelto = float(vuelto)
            lavanderia.fecha_hora_salida = timezone.now()

            lavanderia.save()
            print(lavanderia.fecha_hora_salida)

            return HttpResponseRedirect(reverse('historial_lavanderia'))
        except ValueError:
            return HttpResponseBadRequest("Datos inválidos.")
    
    return HttpResponseBadRequest("Método no permitido.")















