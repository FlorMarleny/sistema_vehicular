from django.db import models
from tarifas_vehiculos.models import TarifaVehiculo
from django.utils import timezone


class Conductor(models.Model):
    dni = models.CharField(max_length=8)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()


class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    serie = models.CharField(max_length=50)
    propietario = models.CharField(max_length=100)


class Lavanderia(models.Model):
    tarifa_vehiculo = models.ForeignKey(TarifaVehiculo, on_delete=models.CASCADE)
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    lavadero = models.BooleanField(default=False)
    cochera = models.BooleanField(default=False)
 
    total_a_pagar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tiempo = models.CharField(max_length=20, null=True, blank=True)
    precio_cochera = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_hora_entrada = models.DateTimeField(auto_now_add=True)
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)

    efectivo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vuelto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

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
  