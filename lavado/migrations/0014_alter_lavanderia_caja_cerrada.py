# Generated by Django 5.0.3 on 2024-05-26 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lavado', '0013_alter_lavanderia_caja_cerrada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lavanderia',
            name='caja_cerrada',
            field=models.BooleanField(default=False),
        ),
    ]
