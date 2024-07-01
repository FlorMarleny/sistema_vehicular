from django.shortcuts import render, get_object_or_404, redirect
from .models import RegistroCierreCajaLavanderia, RegistroCierreCajaCochera ,Caja
from django.http import JsonResponse
from django.db.models import Sum
from lavado.models import Lavanderia
from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib import messages
from estacionamiento.models import Cochera

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
    transacciones_terminadas_cochera = Cochera.objects.filter(
        estado='terminada', cochera=True, caja_cerrada=False)
    total_transacciones_cochera = transacciones_terminadas_cochera.aggregate(
        total=Sum('precio_cochera'))['total'] or 0

    return render(request, 'caja/cajaCochera/cajaCochera.html', {
        'transacciones_terminadas_cochera': transacciones_terminadas_cochera,
        'total_transacciones_cochera': total_transacciones_cochera,
    })


def cerrar_caja_cochera(request):
    if request.method == 'POST':
        total_cochera_str = request.POST.get('total_cochera', '')
        try:
            total_cochera = float(total_cochera_str)
        except ValueError:
            messages.error(request, "El monto total de cochera no es válido.")
            return redirect('cerrar_caja_cochera')

        # Verificar si hay transacciones de cochera disponibles para cerrar
        transacciones_pendientes = Cochera.objects.filter(estado='terminada', caja_cerrada=False).exists()

        if not transacciones_pendientes:
            messages.error(request, "No hay transacciones de cochera disponibles para cerrar.")
            return redirect('cerrar_caja_cochera')

        try:
            # Actualizar todas las transacciones de cochera en estado "terminado" y caja abierta
            transacciones_terminadas_cochera = Cochera.objects.filter(estado='terminada', caja_cerrada=False)
            transacciones_terminadas_cochera.update(caja_cerrada=True)

            # Crear un registro de cierre de caja de cochera en la base de datos
            RegistroCierreCajaCochera.objects.create(
                monto_transaccion=total_cochera,
                usuario=request.user,  # Asignar el usuario autenticado
                tipo_usuario='tipo de usuario'  # Ajustar según tus necesidades
            )

            messages.success(request, 'Caja de cochera cerrada correctamente.')
            return redirect('historial_caja_cochera')
        
        except Exception as e:
            messages.error(request, f"Error al cerrar la caja: {str(e)}")
            return redirect('cerrar_caja_cochera')

    return render(request, 'caja/cajaCochera/cajaCochera.html')

def cerrar_caja_lavanderia(request):
    if request.method == 'POST':
        total_lavanderia_str = request.POST.get('total_lavanderia', '')
        try:
            total_lavanderia = float(total_lavanderia_str)
        except ValueError:
            messages.error(request, "El monto total de lavandería no es válido.")
            return redirect('cerrar_caja_lavanderia')

        # Verificar si hay transacciones de lavandería disponibles para cerrar
        transacciones_pendientes = Lavanderia.objects.filter(estado='terminada', caja_cerrada=False).exists()

        if not transacciones_pendientes:
            messages.error(request, "No hay transacciones de lavandería disponibles para cerrar.")
            return redirect('cerrar_caja_lavanderia')

        try:
            # Actualizar todas las transacciones de lavandería en estado "terminado" y caja abierta
            transacciones_terminadas_lavanderia = Lavanderia.objects.filter(estado='terminada', caja_cerrada=False)
            transacciones_terminadas_lavanderia.update(caja_cerrada=True)

            # Crear un registro de cierre de caja de lavandería en la base de datos
            RegistroCierreCajaLavanderia.objects.create(
                monto_transaccion=total_lavanderia,
                usuario=request.user,  # Asignar el usuario autenticado
                tipo_usuario='tipo de usuario'  # Ajustar según tus necesidades
            )

            messages.success(request, 'Caja de lavandería cerrada correctamente.')
            return redirect('historial_caja_lavanderia')
        
        except Exception as e:
            messages.error(request, f"Error al cerrar la caja: {str(e)}")
            return redirect('cerrar_caja_lavanderia')

    return render(request, 'caja/cajaLavadero/cajaLavadero.html')


def cajas_cerradas(request):
    cajas_cerradas = Caja.objects.filter(cerrada=True)
    return render(request, 'caja/cajas_cerradas.html', {'cajas_cerradas': cajas_cerradas})

def historial_caja_lavanderia(request):
    try:
        historiales = RegistroCierreCajaLavanderia.objects.all().order_by(
            '-fecha_hora_transaccion')
        total_ingresos = historiales.aggregate(
            total=Sum('monto_transaccion'))['total']
        
        return render(request, 'caja/cajaLavadero/cajaHistorialLavadero.html', {
            'historiales': historiales,
            'total_ingresos': total_ingresos,
        })
    except RegistroCierreCajaLavanderia.DoesNotExist:
        historiales = []
        total_ingresos = 0
        return render(request, 'caja/cajaLavadero/cajaHistorialLavadero.html', {
            'historiales': historiales,
            'total_ingresos': total_ingresos,
            'error_message': 'No hay registros de cierre de caja de lavandería disponibles.'
        })
    except Exception as e:
        print(e)  # Imprimir el error en consola para depuración
        return render(request, 'caja/cajaLavadero/cajaHistorialLavadero.html', {
            'historiales': [],
            'total_ingresos': 0,
            'error_message': 'Error al cargar el historial de caja de lavandería.'
        })

def detalle_caja(request, pk):
    print(f"Recibiendo PK: {pk}")  # Verificar el valor del pk
    caja = get_object_or_404(Caja, pk=pk)
    return render(request, 'caja/cajaDetallesLavadero.html', {'caja': caja})



def historial_caja_cochera(request):
    try:
        historiales = RegistroCierreCajaCochera.objects.all().order_by(
            '-fecha_hora_transaccion')
        total_ingresos = historiales.aggregate(
            total=Sum('monto_transaccion'))['total']
        
        return render(request, 'caja/cajaCochera/cajaHistorialCochera.html', {
            'historiales': historiales,
            'total_ingresos': total_ingresos,
        })
    except RegistroCierreCajaLavanderia.DoesNotExist:
        historiales = []
        total_ingresos = 0
        return render(request, 'caja/cajaCochera/cajaHistorialCochera.html', {
            'historiales': historiales,
            'total_ingresos': total_ingresos,
            'error_message': 'No hay registros de cierre de caja de cochera disponibles.'
        })
    except Exception as e:
        print(e)  # Imprimir el error en consola para depuración
        return render(request, 'caja/cajaCochera/cajaHistorialCochera.html', {
            'historiales': [],
            'total_ingresos': 0,
            'error_message': 'Error al cargar el historial de caja de cochera.'
        })


















