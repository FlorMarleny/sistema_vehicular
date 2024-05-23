from django.db import models

class TarifaVehiculo(models.Model):
    TIPO_VEHICULO_CHOICES = (
        ('Automóvil', 'Automóvil'),
        ('Camioneta', 'Camioneta'),
        ('Moto', 'Moto'),
    )

    tipo_vehiculo = models.CharField(
        max_length=100, choices=TIPO_VEHICULO_CHOICES, unique=True)
    precio_manana = models.DecimalField(max_digits=10, decimal_places=2)
    precio_tarde = models.DecimalField(max_digits=10, decimal_places=2)
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)
    precio_dia_completo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_lavado = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"{self.tipo_vehiculo} - Precios"
