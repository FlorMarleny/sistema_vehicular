# Generated by Django 5.0.3 on 2024-05-26 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0005_rename_nombre_caja_caja_nombre_caja_cerrada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='nombre_caja_cerrada',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
