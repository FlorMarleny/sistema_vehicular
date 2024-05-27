from django.urls import path
from . import views
from .views import cerrar_caja_lavanderia, cerrar_caja_cochera

urlpatterns = [
    path('caja-general/', views.caja_view, name='cajaGeneral'),

    path('cerrar-caja-lavanderia/', cerrar_caja_lavanderia, name='cerrar_caja_lavanderia'),
    path('cerrar-caja-cochera/', cerrar_caja_cochera, name='cerrar_caja_cochera'),


    path('caja-lavanderia/', views.caja_lavanderia, name='cajaLavanderia'),
    path('cajas-cerradas/', views.cajas_cerradas, name='cajas_cerradas'),
    path('detalle-caja/<int:caja_id>/', views.detalle_caja, name='detalle_caja'),
]
