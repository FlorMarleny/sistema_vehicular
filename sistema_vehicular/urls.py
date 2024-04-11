from django.contrib import admin
from django.urls import path, include
from accounts.views import login_view

urlpatterns = [
    path('', login_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('estacionamiento/', include('estacionamiento.urls')),
    path('lavado/', include('lavado.urls')),
    # path('tarifas/', include('tarifas_vehiculos.urls')),
    path('tarifas/', include('tarifas_vehiculos.urls')),  # Incluir las URLs de la aplicación de tarifas de vehículos

    
]
