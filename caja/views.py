from django.shortcuts import render, get_object_or_404, redirect
from .models import RegistroCierreCajaLavanderia, RegistroCierreCajaCochera ,Caja
from django.http import JsonResponse
from django.db.models import Sum
from lavado.models import Lavanderia
from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib import messages
from estacionamiento.models import Cochera
from django.core.paginator import Paginator
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.http import HttpResponse

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




# def reporte_general(request):
#     cocheras = Cochera.objects.filter(estado='terminada')
#     lavanderias = Lavanderia.objects.filter(estado='terminada')
#     return render(request, 'caja/cajaGeneral/reporteGeneral.html', {'cocheras': cocheras, 'lavanderias': lavanderias})

# from django.shortcuts import render
# from .models import Cochera, Lavanderia

def reporte_general(request):
    cocheras = Cochera.objects.filter(estado='terminada').values(
        'vehiculo__placa', 'tarifa_vehiculo__tipo_vehiculo', 'fecha_hora_entrada', 'fecha_hora_salida', 'tiempo', 'total_a_pagar'
    )
    lavanderias = Lavanderia.objects.filter(estado='terminada').values(
        'vehiculo__placa', 'tarifa_vehiculo__tipo_vehiculo', 'fecha_hora_entrada', 'fecha_hora_salida', 'tiempo', 'total_a_pagar'
    )

    # Convertir cocheras y lavanderias a listas y agregar el tipo de servicio
    lista_cocheras = list(cocheras)
    for cochera in lista_cocheras:
        cochera['tipo_servicio'] = 'Cochera'

    lista_lavanderias = list(lavanderias)
    for lavanderia in lista_lavanderias:
        lavanderia['tipo_servicio'] = 'Lavandería'

    # Unir las dos listas
    servicios = lista_cocheras + lista_lavanderias
    
        # Calcular el total general
    total_general = sum(servicio['total_a_pagar'] for servicio in servicios)

    # Implementar paginación
    paginator = Paginator(servicios, 10)  # Mostrar 10 servicios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'caja/cajaGeneral/reporteGeneral.html', {'servicios': servicios , 'page_obj': page_obj,'total_general': total_general})




def generar_pdf_reporte_general(request):
    # Obtener todos los registros de Cochera y Lavanderia terminados
    cocheras = Cochera.objects.filter(estado='terminada').values(
        'vehiculo__placa', 'tarifa_vehiculo__tipo_vehiculo', 'fecha_hora_entrada', 'fecha_hora_salida', 'tiempo', 'total_a_pagar'
    )
    lavanderias = Lavanderia.objects.filter(estado='terminada').values(
        'vehiculo__placa', 'tarifa_vehiculo__tipo_vehiculo', 'fecha_hora_entrada', 'fecha_hora_salida', 'tiempo', 'total_a_pagar'
    )

    # Unir cocheras y lavanderias en una lista
    servicios = list(cocheras) + list(lavanderias)

    # Calcular el total general
    total_general = sum(servicio['total_a_pagar'] for servicio in servicios)

    # Configuración de estilos para el PDF
    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_table = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ])

    # Contenido del PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_general.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Título del documento
    elements.append(Paragraph("Reporte General de Servicios", style_title))
    elements.append(Paragraph(f"Total General: S/ {total_general}", style_title))
    elements.append(Paragraph("", style_title))

    # Tabla de servicios
    data = [['Placa', 'Tipo de Vehículo', 'Fecha y Hora de Entrada', 'Fecha y Hora de Salida', 'Tiempo', 'Total a Pagar']]
    for servicio in servicios:
        data.append([
            servicio['vehiculo__placa'],
            servicio['tarifa_vehiculo__tipo_vehiculo'],
            servicio['fecha_hora_entrada'].strftime('%d-%m-%Y %H:%M:%S'),
            servicio['fecha_hora_salida'].strftime('%d-%m-%Y %H:%M:%S') if servicio['fecha_hora_salida'] else '-',
            servicio['tiempo'] if servicio['tiempo'] else '-',
            f"S/ {servicio['total_a_pagar']}"
        ])

    # Crear tabla y aplicar estilos
    table = Table(data)
    table.setStyle(style_table)
    elements.append(table)

    # Construir el PDF
    doc.build(elements)
    return response



