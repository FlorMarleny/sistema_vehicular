from django.db import models
from tarifas_vehiculos.models import TarifaVehiculo
from django.utils import timezone
import barcode
from barcode.writer import ImageWriter


class Conductor(models.Model):
    dni = models.CharField(max_length=8)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    propietario = models.CharField(max_length=100)

    def __str__(self):
        return self.placa


class Lavanderia(models.Model):
    ESTADOS = (
        ('en_proceso', 'En proceso'),
        ('terminada', 'Terminada'),
    )

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
    estado = models.CharField(max_length=20, choices=ESTADOS, default='en_proceso')
    caja_cerrada = models.BooleanField(default=False)

    codigo_barras = models.ImageField(upload_to='codigos_barras/', blank=True)

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

    def save(self, *args, **kwargs):
        if not self.pk:
            codigo = f'{self.vehiculo.placa}-{self.conductor.dni}-{timezone.now().strftime("%Y%m%d")}'
            ean = barcode.get_barcode_class('code128')
            codigo_barras = ean(codigo, writer=ImageWriter())
            archivo_imagen = codigo_barras.save('codigo_barras')
            self.codigo_barras = archivo_imagen

        self.total_a_pagar = self.calcular_total_a_pagar()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lavandería - {self.vehiculo.placa}"
