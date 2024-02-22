# swappable_models.py
from django.db import models
from django.db.models.signals import m2m_changed
from decimal import Decimal, ROUND_HALF_UP
from DistribuidoraCarne.validaciones import *
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone  import now
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db import models

class Cotizacion(models.Model):
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, verbose_name="Cliente")
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    fecha_cotizacion = models.DateField(auto_now = True, validators=[validar_fecha_actualizacion])
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Empleado")
    def save(self, *args, **kwargs):

        if not self.usuario:
            # Si el campo usuario no tiene valor, establecemos el usuario en línea actual
            user_model = get_user_model()
            self.usuario = user_model.objects.get(pk=1)  # Puedes ajustar esto según tu lógica para obtener el usuario en línea
    
    class Meta:
        verbose_name = 'Cotizacion'
        verbose_name_plural = 'Cotizaciones'  
    
    def __str__(self):
        return str(self.id_cliente.nombre) 