from django.urls import path
from .views import estacionamiento_view, editar_cochera, detalles_cochera, eliminar_cochera
from . import views

urlpatterns = [
    path('', estacionamiento_view, name='estacionamiento'),
    path('estacionamiento/editar-cochera/<int:id>/', editar_cochera, name='editar_cochera'),
    path('estacionamiento/detalles-cochera/<int:id>/', detalles_cochera, name='detalles_cochera'),
    path('estacionamiento/eliminar-cochera/<int:id>/', eliminar_cochera, name='eliminar_cochera'),
    path('acceder_salida_cochera/', views.acceder_salida_cochera, name='acceder_salida_cochera'),
    path('historial-cochera/', views.historial_cochera, name='historial_cochera'),
]
