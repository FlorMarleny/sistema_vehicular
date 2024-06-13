# Generated by Django 5.0.3 on 2024-06-13 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cochera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lavadero', models.BooleanField(default=False)),
                ('cochera', models.BooleanField(default=False)),
                ('total_a_pagar', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tiempo', models.CharField(blank=True, max_length=20, null=True)),
                ('precio_cochera', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fecha_hora_entrada', models.DateTimeField(auto_now_add=True)),
                ('fecha_hora_salida', models.DateTimeField(blank=True, null=True)),
                ('efectivo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vuelto', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('estado', models.CharField(choices=[('en_proceso', 'En proceso'), ('terminada', 'Terminada')], default='en_proceso', max_length=20)),
                ('caja_cerrada', models.BooleanField(default=False)),
            ],
        ),
    ]