from django.shortcuts import get_object_or_404
from .forms import BusquedaTarifaForm
from django.shortcuts import render, redirect
from .forms import TarifaVehiculoForm
from .models import TarifaVehiculo


def registrar_tarifa_vehiculo(request):
    if request.method == 'POST':
        form = TarifaVehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_tarifa_vehiculo')
    else:
        form = TarifaVehiculoForm()

    tarifas = TarifaVehiculo.objects.all()
    return render(request, 'tarifas/tarifavehiculos.html', {'form': form, 'tarifas': tarifas})


def lista_tarifas(request):
    form = BusquedaTarifaForm(request.GET)
    tarifas = TarifaVehiculo.objects.all()

    if form.is_valid():
        query = form.cleaned_data['q']
        if query:
            tarifas = tarifas.filter(tipo_vehiculo__icontains=query)
    return render(request, 'tarifas/tarifavehiculos.html', {'tarifas': tarifas, 'form': form})


def editar_tarifa_vehiculo(request, id):
    tarifa = get_object_or_404(TarifaVehiculo, id=id)
    if request.method == 'POST':
        form = TarifaVehiculoForm(request.POST, instance=tarifa)
        if form.is_valid():
            form.save()
            return redirect('registrar_tarifa_vehiculo')
    else:
        form = TarifaVehiculoForm(instance=tarifa)
    return render(request, 'editar_tarifa.html', {'form': form})


def eliminar_tarifa_vehiculo(request, id):
    tarifa = get_object_or_404(TarifaVehiculo, id=id)
    tarifa.delete()
    return redirect('registrar_tarifa_vehiculo')
