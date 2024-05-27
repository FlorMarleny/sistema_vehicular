from django.urls import path
from .views import estacionamiento_view

urlpatterns = [
    path('', estacionamiento_view, name='estacionamiento'),
]

