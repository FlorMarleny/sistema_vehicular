from django.urls import path
from .views import lavado_view
from .views import registro_lavanderia 
from . import views
from .views import obtener_nombres_apellidos_por_dni , obtener_precio
from .views import editar_lavanderia, detalles_lavanderia, eliminar_lavanderia

urlpatterns = [
    path('', lavado_view, name='lavado'),
    path('registro/', views.registro_lavanderia, name='registro_lavanderia'),
    path('registro-lavanderia/', registro_lavanderia, name='registro_lavanderia'),
    path('historial-lavanderia/', views.historial_lavanderia, name='historial_lavanderia'),
    path('registro/obtener-nombres-apellidos/', views.obtener_nombres_apellidos_por_dni, name='obtener_nombres_apellidos'),
    path('obtener-precio/', obtener_precio, name='obtener_precio'),
    path('historial-cochera/', views.historial_cochera, name='historial_cochera'),

    path('lavado/editar-lavanderia/<int:id>/', editar_lavanderia, name='editar_lavanderia'),
    path('lavado/detalles-lavanderia/<int:id>/', detalles_lavanderia, name='detalles_lavanderia'),
    path('lavado/eliminar-lavanderia/<int:id>/', eliminar_lavanderia, name='eliminar_lavanderia'),
  



]
