from django.shortcuts import render, get_object_or_404, redirect
from .models import RegistroCierreCajaLavanderia, RegistroCierreCajaCochera ,Caja
from django.http import JsonResponse
# from .models import Lavanderia, Caja
from django.db.models import Sum
from lavado.models import Lavanderia
from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib import messages


def caja_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cajaGeneral')
        else:
            messages.error(
                request, 'Credenciales inválidas. Inténtalo de nuevo.')
    return render(request, 'caja/loginCaja.html')

def caja_view(request):
    cajas = Caja.objects.all()
    return render(request, 'caja/cajaGeneral.html', {'cajas': cajas})

def caja_lavanderia(request):
    transacciones_terminadas_lavanderia = Lavanderia.objects.filter(
        estado='terminada', caja_cerrada=False)
    total_transacciones_lavanderia = transacciones_terminadas_lavanderia.aggregate(
        total=Sum('tarifa_vehiculo__precio_lavado'))['total'] or 0

    return render(request, 'caja/cajaLavadero/cajaLavadero.html', {
        'transacciones_terminadas_lavanderia': transacciones_terminadas_lavanderia,
        'total_transacciones_lavanderia': total_transacciones_lavanderia,
    })

def caja_cochera(request):
    transacciones_terminadas_cochera = Lavanderia.objects.filter(
        estado='terminada', cochera=True, caja_cerrada=False)
    total_transacciones_cochera = transacciones_terminadas_cochera.aggregate(
        total=Sum('precio_cochera'))['total'] or 0

    return render(request, 'caja/cajaCochera/cajaCochera.html', {
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
        transacciones_terminadas_lavanderia = Lavanderia.objects.filter(
            estado='terminada', caja_cerrada=False)
        transacciones_terminadas_lavanderia.update(caja_cerrada=True)
        # Guardar el registro de cierre de caja de lavandería en la base de datos
        RegistroCierreCajaLavanderia.objects.create(
            monto_transaccion=total_lavanderia)
        return JsonResponse({'message': 'Caja de lavandería cerrada correctamente.'})
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def cajas_cerradas(request):
    cajas_cerradas = Caja.objects.filter(cerrada=True)
    return render(request, 'caja/cajas_cerradas.html', {'cajas_cerradas': cajas_cerradas})

def historial_caja_lavanderia(request):
    historiales = RegistroCierreCajaLavanderia.objects.all().order_by(
        '-fecha_hora_transaccion')
    total_ingresos = historiales.aggregate(
        total=models.Sum('monto_transaccion'))['total']
    return render(request, 'caja/cajaLavadero/cajaHistorialLavadero.html', {'historiales': historiales, 'total_ingresos': total_ingresos})

def detalle_caja(request, pk):
    print(f"Recibiendo PK: {pk}")  # Verificar el valor del pk
    caja = get_object_or_404(Caja, pk=pk)
    return render(request, 'caja/cajaDetallesLavadero.html', {'caja': caja})


# def historial_caja_cochera(request):
#     historiales = Cochera.objects.filter(
#         estado='terminada').order_by('-fecha_hora_salida')
#     total_ingresos = sum(historial.total_a_pagar for historial in historiales)
#     return render(request, 'historiales/historial_caja_cochera.html', {
#         'historiales': historiales,
#         'total_ingresos': total_ingresos
#     })
