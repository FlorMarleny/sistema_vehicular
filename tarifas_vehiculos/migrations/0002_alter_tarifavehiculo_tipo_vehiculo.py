# Generated by Django 5.0.3 on 2024-04-25 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarifas_vehiculos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarifavehiculo',
            name='tipo_vehiculo',
            field=models.CharField(choices=[('Automóvil', 'Automóvil'), ('Camioneta', 'Camioneta'), ('Moto', 'Moto')], max_length=100, unique=True),
        ),
    ]