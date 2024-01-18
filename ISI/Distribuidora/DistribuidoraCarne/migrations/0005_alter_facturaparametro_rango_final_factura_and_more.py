# Generated by Django 4.2.7 on 2024-01-05 02:38

import DistribuidoraCarne.validaciones
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DistribuidoraCarne', '0004_remove_historicalsucursal_inventario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturaparametro',
            name='rango_final_factura',
            field=models.CharField(max_length=16, verbose_name='Rango Final Factura'),
        ),
        migrations.AlterField(
            model_name='facturaparametro',
            name='rango_inicial_factura',
            field=models.CharField(max_length=16, validators=[DistribuidoraCarne.validaciones.validar_rango_inicial], verbose_name='Rango Inicial Factura'),
        ),
    ]