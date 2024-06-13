from django.db import models
from tarifas_vehiculos.models import TarifaVehiculo
from django.utils import timezone
from lavado.models import Conductor, Vehiculo


class Cochera(models.Model):
    ESTADOS = (
        ('en_proceso', 'En proceso'),
        ('terminada', 'Terminada'),
    )

    tarifa_vehiculo = models.ForeignKey(
        TarifaVehiculo, on_delete=models.CASCADE)
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    
    lavadero = models.BooleanField(default=False)
    cochera = models.BooleanField(default=False)

    total_a_pagar = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    tiempo = models.CharField(max_length=20, null=True, blank=True)
    precio_cochera = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_hora_entrada = models.DateTimeField(auto_now_add=True)
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)
    efectivo = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    vuelto = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    estado = models.CharField(
        max_length=20, choices=ESTADOS, default='en_proceso')
    caja_cerrada = models.BooleanField(default=False)

    def registrar_salida(self):
        self.fecha_hora_salida = timezone.now()
        self.save()

    def calcular_total_a_pagar(self):
        total = 0
        if self.lavadero:
            total += self.tarifa_vehiculo.precio_lavado
        if self.cochera:
            total += self.precio_cochera or 0
        return total

    def __str__(self):
        return f"Cochera - {self.vehiculo.placa}"
