from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import LavanderiaForm, ConductorForm, VehiculoForm
from django.views.decorators.csrf import csrf_exempt
import requests
from tarifas_vehiculos.models import TarifaVehiculo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse
from .models import Lavanderia, Conductor, Vehiculo
from estacionamiento.models import Cochera as EstacionamientoCochera

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from estacionamiento.models import Cochera


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

    context = {
        'form': form,
        'tipos_vehiculo': tipos_vehiculo
    }
    return render(request, 'lavanderia/registrarLavanderia.html', context)


def historial_lavanderia(request):
    query = request.GET.get('q')
    lavanderias = Lavanderia.objects.filter(
        lavadero=True).order_by('-fecha_hora_entrada').order_by('-fecha_hora_entrada')
    total_registros = lavanderias.count()

    if query:
        lavanderias = lavanderias.filter(
            Q(conductor__nombres__icontains=query) |
            Q(conductor__apellidos__icontains=query) |
            Q(vehiculo__placa__icontains=query) |
            Q(tarifa_vehiculo__tipo_vehiculo__icontains=query)
        )
    paginator = Paginator(lavanderias, 10)
    page_number = request.GET.get('page')

    try:
        lavanderias = paginator.page(page_number)
    except PageNotAnInteger:
        lavanderias = paginator.page(1)
    except EmptyPage:
        lavanderias = paginator.page(paginator.num_pages)

    context = {
        'lavanderias': lavanderias,
        'total_registros': total_registros
    }
    return render(request, 'lavanderia/historialLavanderia.html', context)


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

            if not request.POST.get('lavadero') and not request.POST.get('cochera'):
                messages.error(
                    request, 'Debe seleccionar al menos Lavadero o Cochera.')
                context = {
                    'lavanderia_form': lavanderia_form,
                    'conductor_form': conductor_form,
                    'vehiculo_form': vehiculo_form,
                    'tarifas_vehiculo': tarifas_vehiculo,
                }
                return render(request, 'lavanderia/registrarLavanderia.html', context)

            dni = conductor_form.cleaned_data['dni']
            placa = vehiculo_form.cleaned_data['placa']

            # Verificar si el conductor ya existe
            try:
                conductor = Conductor.objects.get(dni=dni)
            except Conductor.DoesNotExist:
                conductor = conductor_form.save()

            # Verificar si el vehículo ya existe, si no existe, guardarlo
            try:
                vehiculo = Vehiculo.objects.get(placa=placa)
            except Vehiculo.DoesNotExist:
                vehiculo = vehiculo_form.save()

            # Si hay múltiples vehículos con la misma placa, elegir el primero (o decidir cómo manejar este caso)
            except Vehiculo.MultipleObjectsReturned:
                vehiculo = Vehiculo.objects.filter(placa=placa).first()

            lavanderia = lavanderia_form.save(commit=False)
            lavanderia.conductor = conductor
            lavanderia.vehiculo = vehiculo

            if 'tarifa_vehiculo' in request.POST and 'tiempo' in request.POST:
                tarifa_vehiculo_id = request.POST.get('tarifa_vehiculo')
                tiempo = request.POST.get('tiempo')
                try:
                    tarifa_vehiculo = TarifaVehiculo.objects.get(
                        id=tarifa_vehiculo_id)
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

                    # Guardar en la base de datos de estacionamiento si se selecciona cochera
                    if 'cochera' in request.POST:
                        print("Se seleccionó cochera.")
                        estacionamiento_cochera = EstacionamientoCochera.objects.create(
                            tarifa_vehiculo=tarifa_vehiculo,
                            conductor=conductor,
                            vehiculo=vehiculo,
                            cochera=True,
                            total_a_pagar=lavanderia.total_a_pagar,
                            tiempo=tiempo,
                            precio_cochera=lavanderia.precio_cochera,
                            fecha_hora_entrada=lavanderia.fecha_hora_entrada,
                            estado=lavanderia.estado,
                            caja_cerrada=lavanderia.caja_cerrada
                        )
                        estacionamiento_cochera.save()
                        print("Cochera también guardada en estacionamiento.")

                    # Guardar en la base de datos de lavado si se selecciona lavadero
                    if 'lavadero' in request.POST:
                        print("Se seleccionó lavadero.")
                        lavanderia.save()
                        print("Lavandería también guardada en lavado.")

                    messages.success(request, 'Registro exitoso.')

                    # Redirigir después de guardar
                    return redirect('registro_lavanderia')

                except TarifaVehiculo.DoesNotExist:

                    messages.error(
                        request, 'Tarifa de vehículo no encontrada.')

            else:
                messages.error(
                    request, 'Debe seleccionar una tarifa y un tiempo para el vehículo.')
        else:
            error_messages = []
            if not lavanderia_form.is_valid():
                error_messages.append('Error en el formulario de lavandería.')
            if not conductor_form.is_valid():
                error_messages.append('Error en el formulario de conductor.')
            if not vehiculo_form.is_valid():
                error_messages.append('Error en el formulario de vehículo.')

            for error in error_messages:
                messages.error(request, error)

            context = {
                'lavanderia_form': lavanderia_form,
                'conductor_form': conductor_form,
                'vehiculo_form': vehiculo_form,
                'tarifas_vehiculo': tarifas_vehiculo,
            }
            return render(request, 'lavanderia/registrarLavanderia.html', context)
    else:
        lavanderia_form = LavanderiaForm()
        conductor_form = ConductorForm()
        vehiculo_form = VehiculoForm()

    context = {
        'lavanderia_form': lavanderia_form,
        'conductor_form': conductor_form,
        'vehiculo_form': vehiculo_form,
        'tarifas_vehiculo': tarifas_vehiculo,
    }
    return render(request, 'lavanderia/registrarLavanderia.html', context)


def editar_lavanderia(request, id):
    lavanderia = get_object_or_404(Lavanderia, id=id)
    tarifas_vehiculo = TarifaVehiculo.objects.all()

    if request.method == 'POST':
        lavanderia_form = LavanderiaForm(request.POST, instance=lavanderia)
        conductor_form = ConductorForm(
            request.POST, instance=lavanderia.conductor)
        vehiculo_form = VehiculoForm(
            request.POST, instance=lavanderia.vehiculo)

        if lavanderia_form.is_valid() and conductor_form.is_valid() and vehiculo_form.is_valid():
            lavanderia = lavanderia_form.save(commit=False)
            conductor = conductor_form.save()
            vehiculo = vehiculo_form.save()

            if 'tarifa_vehiculo' in request.POST and 'tiempo' in request.POST:
                tarifa_vehiculo_id = request.POST.get('tarifa_vehiculo')
                tiempo = request.POST.get('tiempo')
                try:
                    tarifa_vehiculo = TarifaVehiculo.objects.get(
                        id=tarifa_vehiculo_id)
                    lavanderia.tarifa_vehiculo = tarifa_vehiculo
                    lavanderia.tiempo = tiempo

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
                    pass
    else:
        lavanderia_form = LavanderiaForm(instance=lavanderia)
        conductor_form = ConductorForm(instance=lavanderia.conductor)
        vehiculo_form = VehiculoForm(instance=lavanderia.vehiculo)

    context = {
        'lavanderia': lavanderia,
        'lavanderia_form': lavanderia_form,
        'conductor_form': conductor_form,
        'vehiculo_form': vehiculo_form,
        'tarifas_vehiculo': tarifas_vehiculo,
    }
    return render(request, 'lavanderia/editar_lavanderia.html', context)


def detalles_lavanderia(request, id):
    lavanderia = get_object_or_404(Lavanderia, id=id)
    context = {
        'lavanderia': lavanderia
    }
    return render(request, 'lavanderia/detalles_lavanderia.html', context)


def eliminar_lavanderia(request, id):
    if request.method == 'POST':
        lavanderia = get_object_or_404(Lavanderia, id=id)
        lavanderia.delete()
        return JsonResponse({'message': 'Lavanderia eliminada con éxito'})

    # Si no es una solicitud POST, devuelve un error
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def salidas(request):
    if request.method == 'GET':
        numero_dni = request.GET.get('numero_dni', '')

        if not numero_dni:
            return render(request, 'salidas/salidas.html', {'error': 'Ingrese un número de DNI para realizar la búsqueda'})

        lavanderia_resultados = Lavanderia.objects.filter(
            conductor__dni=numero_dni).order_by('-fecha_hora_entrada')
        cochera_resultados = Cochera.objects.filter(
            conductor__dni=numero_dni).order_by('-fecha_hora_entrada')

        combinados = {}

        # Función para redondear las fechas al segundo
        def round_to_second(dt):
            return dt.replace(microsecond=0)

        # Procesar resultados de Lavanderia
        for lav in lavanderia_resultados:
            llave = (round_to_second(lav.fecha_hora_entrada), lav.conductor.dni)

            if llave in combinados:
                combinados[llave]['servicio'] += ' y Lavadero'
                combinados[llave]['total_a_pagar'] += lav.total_a_pagar
            else:
                combinados[llave] = {
                    'conductor': lav.conductor,
                    'vehiculo': lav.vehiculo,
                    'fecha_hora_entrada': lav.fecha_hora_entrada,
                    'fecha_hora_salida': lav.fecha_hora_salida,
                    'servicio': 'Lavadero',
                    'total_a_pagar': lav.total_a_pagar,
                    'estado': lav.estado,
                    'id': lav.id,
                }

        # Procesar resultados de Cochera
        for coch in cochera_resultados:
            llave = (round_to_second(coch.fecha_hora_entrada),
                     coch.conductor.dni)
            if llave in combinados:
                combinados[llave]['servicio'] += ' y Cochera'
                combinados[llave]['total_a_pagar'] += coch.total_a_pagar
            else:
                combinados[llave] = {
                    'conductor': coch.conductor,
                    'vehiculo': coch.vehiculo,
                    'fecha_hora_entrada': coch.fecha_hora_entrada,
                    'fecha_hora_salida': coch.fecha_hora_salida,
                    'servicio': 'Cochera',
                    'total_a_pagar': coch.total_a_pagar,
                    'estado': coch.estado,
                    'id': coch.id,
                }

        resultados_combinados = list(combinados.values())

        print("Resultados combinados:", resultados_combinados)

        return render(request, 'salidas/salidas.html', {'resultados': resultados_combinados})

    return HttpResponseBadRequest("Método no permitido")


def acceder_salida(request):
    if request.method == 'GET':
        lavanderia_id = request.GET.get('id')
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
            lavanderia.estado = 'terminada'
            lavanderia.save()
            print(lavanderia.fecha_hora_salida)

            return HttpResponseRedirect(reverse('historial_lavanderia'))
        except ValueError:
            return HttpResponseBadRequest("Datos inválidos.")

    return HttpResponseBadRequest("Método no permitido.")

 
def generar_pdf_lavadero(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="registro_lavadero.pdf"'

    # Filtrar solo lavanderías con estado 'terminada'
    lavanderias = Lavanderia.objects.filter(estado='terminada')

    # Calcular el total de todos los registros
    total_general = sum(
        lav.tarifa_vehiculo.precio_lavado if lav.tarifa_vehiculo else 0 for lav in lavanderias)

    # Crear un objeto Story (flujo) para contener todos los elementos del PDF
    story = []

    # Definir estilos para el contenido y los párrafos
    styles = getSampleStyleSheet()
    estilo_normal = styles['Normal']
    estilo_titulo = styles['Heading1']

    # Estilo personalizado para los párrafos
    estilo_parrafo = ParagraphStyle(
        'estilo_parrafo',
        parent=estilo_normal,
        fontSize=12,
        spaceBefore=10,
        spaceAfter=10,
    )

    # Agregar el título
    titulo = "<h1 style='text-align: center;'>HISTORIAL DE REGISTRO DE LAVANDERÍA</h1>"
    story.append(Paragraph(titulo, estilo_titulo))
    story.append(Paragraph(
        f"<p style='text-align: center;'><strong>Total general: S/ {total_general}</strong></p>", estilo_parrafo))

    # Definir el estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Encabezado de fondo
        # Alineación centrada para todas las celdas
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Líneas de la cuadrícula
        # Fuente Helvetica para toda la tabla
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        # Tamaño de fuente más grande para la fila de encabezado
        ('FONTSIZE', (0, 0), (-1, 0), 12),
    ])

    # Crear una lista de datos para la tabla
    data = [['Placa', 'Vehículo', 'DNI',
             'Conductor', 'fecha_hora_entrada', 'Precio']]

    # Llenar la lista de datos con los registros de lavandería
    for lavanderia in lavanderias:
        precio_lavado = lavanderia.tarifa_vehiculo.precio_lavado if lavanderia.tarifa_vehiculo else 'No disponible'

        # Agregar el símbolo "S/" antes del precio
        if isinstance(precio_lavado, (int, float)):
            precio_lavado = f"S/ {precio_lavado}"

        data.append([
            lavanderia.vehiculo.placa,
            lavanderia.tarifa_vehiculo.tipo_vehiculo if lavanderia.tarifa_vehiculo else 'No disponible',
            lavanderia.conductor.dni,
            f"{lavanderia.conductor.nombres} {lavanderia.conductor.apellidos}",

            str(precio_lavado),
        ])

    # Agregar la tabla al Story con el estilo definido
    tabla = Table(data)
    tabla.setStyle(style)
    story.append(tabla)

    # Crear el documento PDF y agregar el flujo de elementos (Story)
    doc = SimpleDocTemplate(response, pagesize=letter)
    doc.build(story)

    return response
