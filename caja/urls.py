from django.urls import path
from . import views
from .views import cerrar_caja_lavanderia, historial_caja_lavanderia

urlpatterns = [
    
    path('caja/login/', views.caja_login, name='caja_login'),
    path('caja-general/', views.caja_view, name='cajaGeneral'),
    path('cerrar-caja-lavanderia/', cerrar_caja_lavanderia, name='cerrar_caja_lavanderia'),
    path('caja-lavanderia/', views.caja_lavanderia, name='cajaLavanderia'),
    path('caja/cerrar-caja-cochera/', views.cerrar_caja_cochera, name='cerrar_caja_cochera'),
    path('caja/caja-cochera/', views.caja_cochera, name='caja_cochera'),
    path('cajas-cerradas/', views.cajas_cerradas, name='cajas_cerradas'),
    path('detalle-caja/<int:caja_id>/', views.detalle_caja, name='detalle_caja'),
    path('historial-caja-lavanderia/', historial_caja_lavanderia, name='historial_caja_lavanderia'),
    path('detalle-caja/<int:pk>/', views.detalle_caja, name='detalle_caja'),

]
