# Generated by Django 5.0.3 on 2024-05-26 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroCierreCajaCochera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_transaccion', models.DateTimeField(auto_now_add=True)),
                ('monto_transaccion', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroCierreCajaLavanderia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_transaccion', models.DateTimeField(auto_now_add=True)),
                ('monto_transaccion', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
