from django.db import models

# Create your models here.
from django.db import models

class Lavanderia(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        app_label = 'lavado' 