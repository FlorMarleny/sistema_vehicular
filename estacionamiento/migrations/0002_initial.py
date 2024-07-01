# Generated by Django 5.0.3 on 2024-06-29 20:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estacionamiento', '0001_initial'),
        ('lavado', '0001_initial'),
        ('tarifas_vehiculos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cochera',
            name='conductor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lavado.conductor'),
        ),
        migrations.AddField(
            model_name='cochera',
            name='tarifa_vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tarifas_vehiculos.tarifavehiculo'),
        ),
        migrations.AddField(
            model_name='cochera',
            name='vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lavado.vehiculo'),
        ),
    ]
