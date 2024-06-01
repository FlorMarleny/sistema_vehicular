from django.urls import path
from .views import estacionamiento_view , registro_cochera
from django.urls import path
from . import views

urlpatterns = [
    path('', estacionamiento_view, name='estacionamiento'),
        # path('registro_servicios/', views.registrar_servicios, name='registro_servicios'),
    path('registro-cochera/', registro_cochera, name='registro_cochera'),

]

