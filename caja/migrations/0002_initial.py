# Generated by Django 5.0.3 on 2024-06-13 05:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('caja', '0001_initial'),
        ('lavado', '0001_initial'),
        ('tarifas_vehiculos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='caja',
            name='conductor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lavado.conductor'),
        ),
        migrations.AddField(
            model_name='caja',
            name='lavanderia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lavado.lavanderia'),
        ),
        migrations.AddField(
            model_name='caja',
            name='tarifa_vehiculo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tarifas_vehiculos.tarifavehiculo'),
        ),
        migrations.AddField(
            model_name='caja',
            name='vehiculo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lavado.vehiculo'),
        ),
    ]
