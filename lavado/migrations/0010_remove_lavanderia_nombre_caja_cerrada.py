# Generated by Django 5.0.3 on 2024-05-26 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lavado', '0009_alter_lavanderia_nombre_caja_cerrada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lavanderia',
            name='nombre_caja_cerrada',
        ),
    ]
