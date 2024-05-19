from django.db import models
from tarifas_vehiculos.models import TarifaVehiculo


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
    fecha_hora_entrada = models.DateTimeField(auto_now_add=True)

