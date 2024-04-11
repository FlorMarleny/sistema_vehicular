from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render
from .models import Lavanderia
import requests
from .utils import ReniecAPI
import json
from django.conf import settings
from django.http import JsonResponse



# views.py

import requests
from django.shortcuts import render
from .models import Lavanderia
from .forms import LavanderiaForm

def registro_lavanderia(request):
    if request.method == 'POST':
        form = LavanderiaForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            nombres, apellidos = obtener_nombres_apellidos(dni)
            if nombres and apellidos:
                lavanderia = form.save(commit=False)
                lavanderia.nombres = nombres
                lavanderia.apellidos = apellidos
                lavanderia.save()
                return render(request, 'lavanderia/historialLavanderia.html')
            else:
                form.add_error('dni', 'No se encontraron datos para el DNI proporcionado')
    else:
        form = LavanderiaForm()
    return render(request, 'lavanderia/registrarLavanderia.html', {'form': form})

def obtener_nombres_apellidos(dni):
    headers = {'Authorization': 'Bearer apis-token-8038.WNWC8hV6ZnDUe2Ku3YF1Z8xVmBo1xscp'}
    response = requests.get(f'https://api.apis.net.pe/v1/dni/{dni}', headers=headers)
    if response.status_code == 200:
        data = response.json().get('data')
        nombres = data.get('nombres')
        apellido_paterno = data.get('apellidoPaterno')
        apellido_materno = data.get('apellidoMaterno')
        apellidos = f'{apellido_paterno} {apellido_materno}'
        return nombres, apellidos
    else:
        return None, None





# def registro_lavanderia(request):
#     if request.method == 'POST':
#         dni = request.POST.get('dni_ruc')  # Obtener el DNI ingresado por el usuario
#         print("DNI ingresado:", dni)  # Imprimir el DNI para verificar en la consola del servidor

#         # Hacer una solicitud a la API con el DNI
#         token = 'apis-token-8037.TsFMsaTEN8z-52LaXTxahFrZW-GTTLqz'  # Tu token aquí
#         url = f'https://api.reniec.com/dni/{dni}'
#         headers = {'Authorization': f'Token {token}'}
        
#         try:
#             response = requests.get(url, headers=headers)
#             data = response.json()
#             print("Datos de la API:", data)  # Imprimir los datos de la API para verificar en la consola del servidor
            
#             # Verificar si se recibieron los datos correctamente
#             if response.status_code == 200:
#                 nombres = data.get('nombres', '')
#                 apellidos = data.get('apellidos', '')
#                 print("Nombres:", nombres)
#                 print("Apellidos:", apellidos)
#             else:
#                 print("Error al obtener los datos de la API")
#         except Exception as e:
#             print("Error al hacer la solicitud a la API:", e)

#     return render(request, 'lavanderia/registrarLavanderia.html')




def reniec_api(request):

    if request.method == 'POST':

        reniec_api = ReniecAPI(token=settings.TOKEN_RENIEC)

        # Request JSON
        data = json.loads(request.body.decode('utf-8'))
        dni = data.get('dni', '')

        try:
            person_info = reniec_api.get_person(dni)

            if person_info:
                return JsonResponse(person_info)
            else:
                return JsonResponse({'error': 'No se encontraron datos para el DNI proporcionado.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': f'Error al consultar la API de reniec/dni: {str(e)}'}, status=500)









def lavado_view(request):
    if request.method == 'POST':
        form = LavanderiaForm(request.POST)
        if form.is_valid():
            # Procesa los datos del formulario aquí
            dni = form.cleaned_data['dni']
            # Resto del código para manejar el formulario...
    else:
        form = LavanderiaForm()
    return render(request, 'lavanderia/registrarLavanderia.html' , {'form': form})


from django.shortcuts import render
from .models import Lavanderia

def historial_lavanderia(request):
    lavanderias = Lavanderia.objects.all()
    return render(request, 'lavanderia/historialLavanderia.html', {'lavanderias': lavanderias})



def obtener_datos_persona(dni, token):
    # Realizar una solicitud a la API para obtener los datos de la persona
    url = f'https://api.reniec.com/dni/{dni}'
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(url, headers=headers)

    # Manejar la respuesta de la API
    if response.status_code == 200:
        data = response.json()
        nombres = data.get('nombres')
        apellidos = data.get('apellidos')
        return nombres, apellidos
    else:
        print(f"Error al obtener los datos de la API: {response.status_code}")

        return None, None




