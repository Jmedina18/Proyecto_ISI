from django.contrib import admin
from .models import *
from django import forms
from django.utils.html import format_html
from django.urls import reverse, reverse_lazy
from .forms import *
from django.urls import path
import csv
from io import StringIO
from simple_history.admin import SimpleHistoryAdmin
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.dispatch import receiver
from django.shortcuts import redirect
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

#Ultimo Cambio

@admin.register(Clientes)
class ClientesAdmin(SimpleHistoryAdmin):
    list_display = ('id','nombre', 'apellido', 'tipo_documento', 'documento', 'telefono', 'correo', 'rtn', 'direccion','fecha_creacion', 'usuario_username')
    search_fields = ['nombre', 'apellido', 'documento', 'telefono', 'correo', 'rtn', 'direccion','fecha_creacion']
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'status', 'fecha_creacion', 'usuario_username')
    search_fields = ('id', 'nombre', 'status', 'fecha_creacion')
    list_filter = ['nombre', 'status', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

@admin.register(MetodosPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'status', 'fecha_creacion', 'usuario_username')
    search_fields = ('id', 'nombre', 'status', 'fecha_creacion')
    list_filter = ['nombre', 'status', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

@admin.register(TipoCargo)
class TipoCargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'status', 'fecha_creacion', 'usuario_username')
    search_fields = ('id', 'nombre', 'status', 'fecha_creacion')
    list_filter = ['nombre', 'status', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'status', 'fecha_creacion', 'usuario_username')
    search_fields = ('id', 'nombre', 'status', 'fecha_creacion')
    list_filter = ['nombre', 'status', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'telefono', 'correo', 'direccion', 'rtn', 'nombre_contacto', 'telefono_contacto', 'fecha_creacion', 'usuario_username')
    search_fields = ('id', 'nombre', 'telefono', 'correo', 'direccion', 'rtn', 'nombre_contacto', 'telefono_contacto')
    list_filter = ['nombre', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

@admin.register(Descuento)
class DescuentoAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'valor', 'fecha_creacion', 'usuario_username')
    search_fields = ('id', 'nombre', 'descripcion', 'valor', 'fecha_creacion')
    list_filter = ['nombre', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

@admin.register(Impuesto)
class ImpuestoAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'valor', 'fecha_creacion', 'usuario_username')
    search_fields = ('id', 'nombre', 'descripcion', 'valor', 'fecha_creacion')
    list_filter = ['nombre', 'fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

@admin.register(Producto)
class ProductoAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'precio_venta', 'categoria', 'proveedor', 'impuesto', 'descuento', 'status', 'fecha_creacion', 'usuario_username')
    search_fields = ('id', 'nombre', 'categoria__nombre', 'status', 'fecha_creacion')
    list_filter = ['categoria', 'proveedor', 'status', 'fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

#puede ser que de error aqui, si da error cambiar los def de producto
@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'cantidad', 'stock_maximo', 'stock_minimo', 'status', 'fecha_creacion', 'usuario_username')
    search_fields = ['id','status', 'fecha_creacion']
    list_filter = ['producto','status', 'fecha_creacion']
    ordering = [  'status', 'cantidad']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario','cantidad']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ciudad', 'direccion', 'telefono', 'rtn', 'status', 'fecha_creacion', 'usuario_username')
    search_fields = ('id', 'nombre', 'ciudad', 'status', 'fecha_creacion')
    list_filter = ['status', 'fecha_creacion']
    ordering = ['nombre', 'ciudad', 'status', 'fecha_creacion']
    filter_horizontal = ('inventarios',)
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

# @receiver(post_save, sender=User)
# def redirigir_a_creacion_empleado(sender, instance, created, **kwargs):
#     if created:
#         # Obtiene el último usuario creado
#         nuevo_usuario = User.objects.latest('id')
#         # Redirige a la vista de Django para crear un nuevo empleado
#         return redirect(reverse('admin:DistribuidoraCarne_empleados_add') + f'?usuario_id={nuevo_usuario.id}')

@admin.register(Empleados)
class EmpleadosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'documento', 'fecha_nacimiento', 'telefono', 'correo', 'direccion', 'status', 'cargo', 'sucursal', 'fecha_creacion', 'usuario_username')
    search_fields = ('id', 'nombre', 'apellido', 'documento', 'status', 'cargo__nombre', 'sucursal__nombre', 'fecha_creacion', 'usuario__username')
    list_filter = ['status', 'cargo', 'sucursal', 'fecha_creacion']
    ordering = ['nombre', 'apellido', 'status', 'fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def add_view(self, request, form_url='', extra_context=None):
        # Si estamos creando un nuevo usuario y estamos logueados como administrador
        if '_addanother' not in request.POST and '_popup' not in request.POST and '_continue' not in request.POST and '_save' in request.POST and request.user.is_superuser:
            # Obtenemos el último usuario creado
            nuevo_usuario = User.objects.latest('id')

            # Asociamos directamente el empleado al último usuario creado
            nuevo_empleado = Empleados(usuario=nuevo_usuario, tipo_documento=TipoDocumento.objects.get(pk=1), nombre='Nombre', apellido='Apellido', documento='Documento', fecha_nacimiento='2022-01-01', telefono='Telefono', correo='Correo', direccion='Direccion', status=True, cargo=TipoCargo.objects.get(pk=1), sucursal=Sucursal.objects.get(pk=1))
            nuevo_empleado.save()

            # Redirige a la vista de cambio del empleado recién creado
            return HttpResponseRedirect(reverse_lazy('admin:distribuidoracarne_empleados', args=[nuevo_empleado.id]))

        # Si no estamos creando un nuevo usuario o no estamos logueados como administrador, utiliza el flujo estándar
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

class CompraForm(admin.TabularInline):
    model = Compra
    can_delete = True
    extra = 1
    autocomplete_fields = ['producto']  # Ajusta esto según tus modelos
    form = CompraForm
   
@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    inlines = [CompraForm]
    list_display = ('id', 'descuento', 'impuesto', 'sub_total', 'total', 'usuario_username')
    list_filter = ['id']
    readonly_fields = ['sub_total', 'descuento', 'impuesto', 'total','usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

# @admin.register(DetalleCompra)
# class DetalleCompraAdmin(admin.ModelAdmin):
#     list_display = ('id', 'descuento', 'impuesto', 'sub_total', 'total')
#     search_fields = ['id']
#     readonly_fields = ['sub_total', 'descuento', 'impuesto', 'total']

#     def sub_total(self, obj):
#         return obj.sub_total

#     def total(self, obj):
#         return obj.total

#     def impuesto(self, obj):
#         return obj.impuesto
    
#     def descuento(self, obj):
#         return obj.descuento
    
#     impuesto.short_description = 'Impuesto'
#     descuento.short_description = 'Descuento'
#     sub_total.short_description = 'Subtotal'
#     total.short_description = 'Total'

@admin.register(ParametroSar)
class ParametroSarAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_inicio', 'numero_fin', 'fecha_creacion', 'usuario_username')
    search_fields = ('id', 'numero_inicio', 'numero_fin')
    list_filter = ('fecha_creacion',)
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)
    
@admin.register(FacturaParametro)
class FacturaEncabezadoAdmin(admin.ModelAdmin):
    form = FacturaParametroForm  # Use the custom form
    list_display = ('sucursal', 'cai', 'fecha_emision', 'fecha_limite', 'rango_inicial_factura', 'rango_final_factura', 'status', 'usuario_username')
    search_fields = ('sucursal', 'cai', 'status')
    list_filter = ('sucursal', 'status')
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['usuario']

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

class DetalleVentaForm(admin.TabularInline):
    model = DetalleVenta
    can_delete = True
    extra = 1
    autocomplete_fields=['producto']
    form = DetalleVentaForm

@admin.register(FacturaDet)
class FacturaDetAdmin(admin.ModelAdmin):
    inlines = [DetalleVentaForm]
    list_display = ('id', 'sub_total', 'descuento', 'impuesto', 'total', 'created_at', 'usuario_username')
    search_fields = ['id']
    list_filter = ('created_at',)
    readonly_fields = ('sub_total', 'descuento', 'impuesto', 'total','usuario')
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)

@admin.register(Rutas)
class RutasAdmin(admin.ModelAdmin):
    list_display = ('id', 'ruta',)
    search_fields = ('id', 'ruta',)

@admin.register(Transporte)
class TransporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'ruta', 'nombre_carro', 'codigo', 'chofer')
    search_fields = ('id', 'ruta', 'nombre_carro', 'codigo', 'chofer')

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('id', 'carro', 'fecha_entrega', 'hora_entrega', 'direccion_entrega')
    search_fields = ('id', 'carro', 'fecha_entrega', 'hora_entrega', 'direccion_entrega')

@admin.register(Devoluciones)
class DevolucionesAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_producto', 'cantidad', 'descripcion', 'fecha_devolucion')
    search_fields = ('id', 'id_producto', 'cantidad', 'descripcion', 'fecha_devolucion')

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_cliente', 'id_producto', 'fecha_cotizacion')
    search_fields = ('id', 'id_cliente', 'id_producto', 'fecha_cotizacion')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_clientes', 'id_producto', 'fecha_pedido', 'total_pedido')
    search_fields = ('id', 'id_clientes', 'id_producto', 'fecha_pedido', 'total_pedido') 
   
def get_context_data(factura):
    detalles_Venta = DetalleVenta.objects.filter(detalle=factura.detalle.id)
    
    datos_factura = {
        'encabezado': {
            'Sucursal': factura.Sucursal,
            'Dirección': factura.direccion,
            'numeroFactura': factura.numeroFactura,
            'fechaPago': factura.fechaPago,
            'horaFactura': factura.hora,
            'idCliente': factura.idCliente,
            'empleado' : factura.idUsuario,
            'cai': factura.idParametros.cai,
            'rtn': factura.rtn,
            'documento': factura.idCliente.documento,
        },
        'factura': factura.factura.all(),
        'detalles': factura.detallefactura_set.all(),
        'detalles_Venta': detalles_Venta,
    }

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'parametros', 'numero_factura', 'cliente', 'tipo_pago', 'fecha_creacion','boton_pdf', 'usuario_username')
    search_fields = ('id', 'numero_factura', 'cliente__nombre',)
    list_filter = ('parametros', 'tipo_pago', 'fecha_creacion', 'cliente__nombre',)
    actions = ['generar_pdf_factura']
    readonly_fields = ['usuario']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'cliente':
            # Establecer el valor por defecto a "Consumidor Final"
            kwargs['initial'] = Clientes.objects.get(nombre='Consumidor Final')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    
    usuario_username.short_description = 'Nombre de Usuario'

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = get_user(request)
        super().save_model(request, obj, form, change)
    
    def boton_pdf(self, obj):
        pdf_url = reverse('descargar_pdf_factura', args=[obj.id])
        print(pdf_url)
        return format_html('<a href="{}" class="btn btn-success">Imprimir</button>', pdf_url)
    
    boton_pdf.short_description = 'PDF Factura'
        
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'numero_factura':
            errors = formfield.error_messages.copy()
            errors['rango_final'] = 'Advertencia: Se ha alcanzado el rango final de facturación.'
            formfield.error_messages = errors
        return formfield
    
    def generar_pdf_factura(self, request, queryset):
        for factura in queryset:
            # Generar el PDF y enviarlo como respuesta al navegador
            template = get_template('factura.html')  # Asegúrate de tener este archivo de plantilla
            context = get_context_data(factura)
            html_content = template.render(context)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="factura_{factura.id}.pdf"'
            pisa_status = pisa.CreatePDF(html_content, dest=response)

            if pisa_status.err:
                return HttpResponse(f'Error al generar el PDF para la factura {factura.id}')

        return response

