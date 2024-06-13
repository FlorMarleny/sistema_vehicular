import requests
from django.shortcuts import render, redirect
from .forms import ConductorForm, VehiculoForm, CocheraForm, LavanderiaForm, ServicioForm
from .models import Conductor, Vehiculo, Cochera
from lavado.models import Lavanderia
from tarifas_vehiculos.models import TarifaVehiculo
from django.utils import timezone


def estacionamiento_view(request):
    return render(request, 'estacionamiento.html')


# def registro_cochera(request):
#     tarifas_vehiculo = TarifaVehiculo.objects.all()

#     if request.method == 'POST':
#         conductor_form = ConductorForm(request.POST)
#         vehiculo_form = VehiculoForm(request.POST)
#         cochera_form = CocheraForm(request.POST)
#         lavanderia_form = LavanderiaForm(request.POST)
#         servicio_form = ServicioForm(request.POST)

#         if conductor_form.is_valid() and vehiculo_form.is_valid() and servicio_form.is_valid():
#             conductor = conductor_form.save()
#             vehiculo = vehiculo_form.save()

#             if servicio_form.cleaned_data['cochera'] and cochera_form.is_valid():
#                 cochera = cochera_form.save(commit=False)
#                 cochera.conductor = conductor
#                 cochera.vehiculo = vehiculo
#                 cochera.fecha_hora_entrada = timezone.now()
#                 cochera.total_a_pagar = cochera.calcular_total_a_pagar()
#                 cochera.save()

#             if servicio_form.cleaned_data['lavanderia'] and lavanderia_form.is_valid():
#                 lavanderia = lavanderia_form.save(commit=False)
#                 lavanderia.conductor = conductor
#                 lavanderia.vehiculo = vehiculo
#                 lavanderia.fecha_hora_entrada = timezone.now()
#                 lavanderia.total_a_pagar = lavanderia.calcular_total_a_pagar()
#                 lavanderia.save()

#             return redirect('registro_cochera')
#         else:
#             error_messages = []
#             if not conductor_form.is_valid():
#                 error_messages.append('Error en el formulario de conductor.')
#             if not vehiculo_form.is_valid():
#                 error_messages.append('Error en el formulario de vehículo.')
#             if not servicio_form.is_valid():
#                 error_messages.append('Error en el formulario de servicio.')
#             if servicio_form.cleaned_data['cochera'] and not cochera_form.is_valid():
#                 error_messages.append('Error en el formulario de cochera.')
#             if servicio_form.cleaned_data['lavanderia'] and not lavanderia_form.is_valid():
#                 error_messages.append('Error en el formulario de lavandería.')

#             context = {
#                 'conductor_form': conductor_form,
#                 'vehiculo_form': vehiculo_form,
#                 'cochera_form': cochera_form,
#                 'lavanderia_form': lavanderia_form,
#                 'servicio_form': servicio_form,
#                 'tarifas_vehiculo': tarifas_vehiculo,
#                 'error_message': ' '.join(error_messages),
#             }
#             return render(request, 'cochera/registrarCochera.html', context)
#     else:
#         conductor_form = ConductorForm()
#         vehiculo_form = VehiculoForm()
#         cochera_form = CocheraForm()
#         lavanderia_form = LavanderiaForm()
#         servicio_form = ServicioForm()

#     context = {
#         'conductor_form': conductor_form,
#         'vehiculo_form': vehiculo_form,
#         'cochera_form': cochera_form,
#         'lavanderia_form': lavanderia_form,
#         'servicio_form': servicio_form,
#         'tarifas_vehiculo': tarifas_vehiculo,
#     }

#     return render(request, 'cochera/registrarCochera.html', context)




from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import ConductorForm, VehiculoForm, CocheraForm, ServicioForm
from .models import Conductor, Vehiculo, Cochera
from tarifas_vehiculos.models import TarifaVehiculo

def registro_cochera(request):
    tarifas_vehiculo = TarifaVehiculo.objects.all()

    if request.method == 'POST':
        conductor_form = ConductorForm(request.POST)
        vehiculo_form = VehiculoForm(request.POST)
        cochera_form = CocheraForm(request.POST)
        
        servicio_form = ServicioForm(request.POST)

        if conductor_form.is_valid() and vehiculo_form.is_valid() and cochera_form.is_valid() and servicio_form.is_valid():
            conductor = conductor_form.save()
            vehiculo = vehiculo_form.save()

            cochera = cochera_form.save(commit=False)
            cochera.conductor = conductor
            cochera.vehiculo = vehiculo
            cochera.fecha_hora_entrada = timezone.now()
            cochera.total_a_pagar = cochera.calcular_total_a_pagar()
            cochera.save()

            return redirect('registro_cochera')
        else:
            error_messages = []
            if not conductor_form.is_valid():
                error_messages.append('Error en el formulario de conductor.')
            if not vehiculo_form.is_valid():
                error_messages.append('Error en el formulario de vehículo.')
            if not cochera_form.is_valid():
                error_messages.append('Error en el formulario de cochera.')
            if not servicio_form.is_valid():
                error_messages.append('Error en el formulario de servicio.')

            context = {
                'conductor_form': conductor_form,
                'vehiculo_form': vehiculo_form,
                'cochera_form': cochera_form,
                'servicio_form': servicio_form,
                'tarifas_vehiculo': tarifas_vehiculo,
                'error_message': ' '.join(error_messages),
            }
            return render(request, 'cochera/registrarCochera.html', context)
    else:
        conductor_form = ConductorForm()
        vehiculo_form = VehiculoForm()
        cochera_form = CocheraForm()
        servicio_form = ServicioForm()

    context = {
        'conductor_form': conductor_form,
        'vehiculo_form': vehiculo_form,
        'cochera_form': cochera_form,
        'servicio_form': servicio_form,
        'tarifas_vehiculo': tarifas_vehiculo,
    }

    return render(request, 'cochera/registrarCochera.html', context)















