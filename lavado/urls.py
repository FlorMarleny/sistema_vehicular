from django.urls import path
from .views import lavado_view , editar_lavanderia, detalles_lavanderia, eliminar_lavanderia,registro_lavanderia 
from . import views
from .views import generar_pdf_lavadero

urlpatterns = [
    path('', lavado_view, name='lavado'),
    path('registro/', views.registro_lavanderia, name='registro_lavanderia'),
    path('registro-lavanderia/', registro_lavanderia, name='registro_lavanderia'),
    path('historial-lavanderia/', views.historial_lavanderia, name='historial_lavanderia'),
    path('registro/obtener-nombres-apellidos/', views.obtener_nombres_apellidos_por_dni, name='obtener_nombres_apellidos'),
    path('lavado/editar-lavanderia/<int:id>/', editar_lavanderia, name='editar_lavanderia'),
    path('lavado/detalles-lavanderia/<int:id>/', detalles_lavanderia, name='detalles_lavanderia'),
    path('lavado/eliminar-lavanderia/<int:id>/', eliminar_lavanderia, name='eliminar_lavanderia'),
    path('salidas/', views.salidas, name='salidas'),
    path('accedersalida/', views.acceder_salida, name='accedersalida'), 
    path('reporte/', generar_pdf_lavadero, name='generar_pdf_lavadero'),   
]
