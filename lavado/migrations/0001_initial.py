# Generated by Django 5.0.3 on 2024-04-27 16:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conductor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=8)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('correo', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=10)),
                ('modelo', models.CharField(max_length=100)),
                ('marca', models.CharField(max_length=100)),
                ('matricula', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=50)),
                ('serie', models.CharField(max_length=50)),
                ('propietario', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Lavanderia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lavadero', models.BooleanField(default=False)),
                ('cochera', models.BooleanField(default=False)),
                ('tipo_vehiculo', models.CharField(max_length=100)),
                ('tiempo', models.CharField(max_length=20)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('conductor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lavado.conductor')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lavado.vehiculo')),
            ],
        ),
    ]
