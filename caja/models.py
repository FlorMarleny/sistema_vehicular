from django.db import models
from tarifas_vehiculos.models import TarifaVehiculo
from lavado.models import Vehiculo, Conductor, Lavanderia
from django.contrib.auth.models import User

class Caja(models.Model):
    TIPO_CHOICES = ( ('lavanderia', 'Lavandería'), ('cochera', 'Cochera'),)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    lavanderia = models.ForeignKey(Lavanderia, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True, blank=True)
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE, null=True, blank=True)
    tarifa_vehiculo = models.ForeignKey(TarifaVehiculo, on_delete=models.CASCADE, null=True, blank=True)
    fecha_hora_transaccion = models.DateTimeField(auto_now_add=True)
    monto_transaccion = models.DecimalField(max_digits=10, decimal_places=2)
    cerrada = models.BooleanField(default=False)

    def __str__(self):
        return f"Caja - {self.id} ({self.tipo})"

class RegistroCierreCajaLavanderia(models.Model):
    fecha_hora_transaccion = models.DateTimeField(auto_now_add=True)
    monto_transaccion = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=50)

    def __str__(self):
        return f"Registro de Cierre de Caja de Lavandería - {self.fecha_hora_transaccion}"
    

class RegistroCierreCajaCochera(models.Model):
    fecha_hora_transaccion = models.DateTimeField(auto_now_add=True)
    monto_transaccion = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=100) 
    
    def __str__(self):
        return f"Registro de Cierre de Caja de Cochera - {self.fecha_hora_transaccion}"
