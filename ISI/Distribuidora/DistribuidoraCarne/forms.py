from django import forms
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Asegúrate de agregar esta línea

class FacturaDetForm(forms.ModelForm):
    class Meta:
        model = FacturaDet
        fields = '__all__'

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = '__all__'
        
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'

class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = '__all__'

class FacturaParametroForm(forms.ModelForm):
    class Meta:
        model = FacturaParametro
        fields = ['sucursal', 'parametros', 'fecha_limite', 'cai', 'rango_inicial_factura', 'rango_final_factura', 'status']
