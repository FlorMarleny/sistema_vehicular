from estacionamiento.forms import CocheraForm, ConductorForm, VehiculoForm
from .models import Cochera
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from tarifas_vehiculos.models import TarifaVehiculo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse


def estacionamiento_view(request):
    return render(request, 'estacionamiento.html')

def historial_cochera(request):
    query = request.GET.get('q')
    cocheras = Cochera.objects.filter(
        cochera=True
    ).order_by('-fecha_hora_entrada')

    total_registros = cocheras.count()

    if query:
        cocheras = cocheras.filter(
            Q(conductor__nombres__icontains=query) |
            Q(conductor__apellidos__icontains=query) |
            Q(vehiculo__placa__icontains=query) |
            Q(tarifa_vehiculo__tipo_vehiculo__icontains=query)
        )

    paginator = Paginator(cocheras, 10)
    page_number = request.GET.get('page')

    try:
        cocheras = paginator.page(page_number)
    except PageNotAnInteger:
        cocheras = paginator.page(1)
    except EmptyPage:
        cocheras = paginator.page(paginator.num_pages)

    context = {
        'cocheras': cocheras,
        'total_registros': total_registros
    }

    return render(request, 'cochera/historialCochera.html', context)

def editar_cochera(request, id):
    cochera = get_object_or_404(Cochera, id=id)
    tarifas_vehiculo = TarifaVehiculo.objects.all()

    if request.method == 'POST':
        cochera_form = CocheraForm(request.POST, instance=cochera)
        conductor_form = ConductorForm(
            request.POST, instance=cochera.conductor)
        vehiculo_form = VehiculoForm(request.POST, instance=cochera.vehiculo)

        if cochera_form.is_valid() and conductor_form.is_valid() and vehiculo_form.is_valid():
            cochera = cochera_form.save(commit=False)
            conductor = conductor_form.save()
            vehiculo = vehiculo_form.save()

            if 'tarifa_vehiculo' in request.POST and 'tiempo' in request.POST:
                tarifa_vehiculo_id = request.POST.get('tarifa_vehiculo')
                tiempo = request.POST.get('tiempo')
                try:
                    tarifa_vehiculo = TarifaVehiculo.objects.get(
                        id=tarifa_vehiculo_id)
                    cochera.tarifa_vehiculo = tarifa_vehiculo
                    cochera.tiempo = tiempo

                    if tiempo == 'manana':
                        cochera.precio_cochera = tarifa_vehiculo.precio_manana
                    elif tiempo == 'tarde':
                        cochera.precio_cochera = tarifa_vehiculo.precio_tarde
                    elif tiempo == 'noche':
                        cochera.precio_cochera = tarifa_vehiculo.precio_noche
                    elif tiempo == 'dia_completo':
                        cochera.precio_cochera = tarifa_vehiculo.precio_dia_completo

                    cochera.total_a_pagar = cochera.calcular_total_a_pagar()
                    cochera.save()

                    print(f"Cochera actualizada correctamente: {cochera.id}")
                    return redirect('historial_cochera')
                except TarifaVehiculo.DoesNotExist:
                    print(
                        f"TarifaVehiculo con ID {tarifa_vehiculo_id} no encontrado.")
                    pass
                except Exception as e:
                    print(f"Error al actualizar cochera: {str(e)}")
                    pass
            else:
                print("Datos de tarifa_vehiculo y tiempo no encontrados en POST.")
        else:
            print("Formularios inválidos.")
    else:
        cochera_form = CocheraForm(instance=cochera)
        conductor_form = ConductorForm(instance=cochera.conductor)
        vehiculo_form = VehiculoForm(instance=cochera.vehiculo)

    context = {
        'cochera': cochera,
        'cochera_form': cochera_form,
        'conductor_form': conductor_form,
        'vehiculo_form': vehiculo_form,
        'tarifas_vehiculo': tarifas_vehiculo,
    }
    return render(request, 'cochera/opciones/editar_cochera.html', context)

def detalles_cochera(request, id):
    cochera = get_object_or_404(Cochera, id=id)
    context = {
        'cochera': cochera
    }
    return render(request, 'cochera/opciones/detalles_cochera.html', context)

def eliminar_cochera(request, id):
    if request.method == 'POST':
        cochera = get_object_or_404(Cochera, id=id)
        cochera.delete()
        return JsonResponse({'message': 'cochera eliminada con éxito'})

    # Si no es una solicitud POST, devuelve un error
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def acceder_salida_cochera(request):
    if request.method == 'GET':
        cochera_id = request.GET.get('cochera_id')
        cochera = get_object_or_404(Cochera, id=cochera_id)

        return render(request, 'salidas/acceder_salida_cochera.html', {'cochera': cochera})

    elif request.method == 'POST':
        cochera_id = request.POST.get('cochera_id')
        cochera = get_object_or_404(Cochera, id=cochera_id)
        efectivo = request.POST.get('efectivo')
        vuelto = request.POST.get('vuelto')

        try:
            cochera.efectivo = float(efectivo)
            cochera.vuelto = float(vuelto)
            cochera.fecha_hora_salida = timezone.now()
            cochera.estado = 'terminada'
            cochera.save()
            print(cochera.fecha_hora_salida)

            return HttpResponseRedirect(reverse('historial_cochera'))
        except ValueError:
            return HttpResponseBadRequest("Datos inválidos.")

    return HttpResponseBadRequest("Método no permitido.")
