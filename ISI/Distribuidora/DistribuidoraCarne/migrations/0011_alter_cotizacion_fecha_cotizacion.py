# Generated by Django 4.2.7 on 2024-02-20 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DistribuidoraCarne', '0010_alter_cotizacion_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='fecha_cotizacion',
            field=models.DateField(auto_now=True),
        ),
    ]
