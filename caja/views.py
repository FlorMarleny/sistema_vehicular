from .models import RegistroCierreCajaLavanderia, RegistroCierreCajaCochera
from django.http import JsonResponse
from .models import Lavanderia, Caja
from django.db.models import Sum
from django.shortcuts import render
from .models import Caja
from lavado.models import Lavanderia

def caja_view(request):
    cajas = Caja.objects.all()
    return render(request, 'caja/cajaGeneral.html', {'cajas': cajas})

def caja_lavanderia(request):
    transacciones_terminadas_lavanderia = Lavanderia.objects.filter(
        estado='terminada', caja_cerrada=False)
    total_transacciones_lavanderia = transacciones_terminadas_lavanderia.aggregate(
        total=Sum('tarifa_vehiculo__precio_lavado'))['total'] or 0

    return render(request, 'caja/cajaLavadero.html', {
        'transacciones_terminadas_lavanderia': transacciones_terminadas_lavanderia,
        'total_transacciones_lavanderia': total_transacciones_lavanderia,
    })

def caja_cochera(request):
    transacciones_terminadas_cochera = Lavanderia.objects.filter(
        estado='terminada', cochera=True, caja_cerrada=False)
    total_transacciones_cochera = transacciones_terminadas_cochera.aggregate(
        total=Sum('precio_cochera'))['total'] or 0

    return render(request, 'caja/cajaCochera.html', {
        'transacciones_terminadas_cochera': transacciones_terminadas_cochera,
        'total_transacciones_cochera': total_transacciones_cochera,
    })

def cerrar_caja_cochera(request):
    if request.method == 'POST':
        total_cochera = float(request.POST.get('total_cochera'))
        RegistroCierreCajaCochera.objects.create(
            monto_transaccion=total_cochera)
        return JsonResponse({'message': 'Caja de cochera cerrada correctamente.'})
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def cerrar_caja_lavanderia(request):
    if request.method == 'POST':
        total_lavanderia = float(request.POST.get('total_lavanderia'))
        # Actualizar todas las transacciones de lavandería en estado "terminado"
        transacciones_terminadas_lavanderia = Lavanderia.objects.filter(estado='terminada', caja_cerrada=False)
        transacciones_terminadas_lavanderia.update(caja_cerrada=True)
        # Guardar el registro de cierre de caja de lavandería en la base de datos
        RegistroCierreCajaLavanderia.objects.create(monto_transaccion=total_lavanderia)
        return JsonResponse({'message': 'Caja de lavandería cerrada correctamente.'})
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def cajas_cerradas(request):
    cajas_cerradas = Caja.objects.filter(cerrada=True)
    return render(request, 'caja/cajas_cerradas.html', {'cajas_cerradas': cajas_cerradas})

def detalle_caja(request, caja_id):
    caja = Caja.objects.get(pk=caja_id)
    return render(request, 'caja/detalle_caja.html', {'caja': caja})
