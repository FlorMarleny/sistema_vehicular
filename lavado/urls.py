from django.urls import path
from .views import lavado_view
from .views import registro_lavanderia 
from . import views

urlpatterns = [
    path('', lavado_view, name='lavado'),
    path('registro/', views.registro_lavanderia, name='registro_lavanderia'),
    path('registro-lavanderia/', registro_lavanderia, name='registro_lavanderia'),
    path('historial-lavanderia/', views.historial_lavanderia, name='historial_lavanderia'),

]
