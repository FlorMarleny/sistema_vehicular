from django.urls import path
from .views import lista_tarifas
from .views import registrar_tarifa_vehiculo
from .import views
urlpatterns = [
    
    path('listar/', lista_tarifas, name='lista_tarifas'),
    path('registrar/', registrar_tarifa_vehiculo, name='registrar_tarifa_vehiculo'),
    path('editar/<int:tarifa_id>/', views.editar_tarifa_vehiculo, name='editar_tarifa_vehiculo'),
    path('eliminar-tarifa/<int:id>/', views.eliminar_tarifa_vehiculo, name='eliminar_tarifa_vehiculo'),

]
