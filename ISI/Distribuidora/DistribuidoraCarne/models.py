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
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.functional import SimpleLazyObject
#from DistribuidoraCarne.swappable_models import Compra

def get_user(request):
    user = None
    if hasattr(request, 'user') and request.user.is_authenticated:
        user = request.user
    return user

def get_current_user(request):
    user = SimpleLazyObject(lambda: get_user(request))
    return user if hasattr(request, 'user') else None

#UltimoCambio
class MetodosPago(models.Model):
    nombre = models.CharField(max_length=50, validators=[validar_nombre],null=False,verbose_name='Nombre metodo de pago')
    descripcion = models.CharField(max_length=40, blank=True, null=True, validators=[validar_descripcion], verbose_name="Descripción")
    status = models.CharField(max_length=2, choices=(('1', 'Activo'), ('2', 'Inactivo')), default='1', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now=True, editable=False,verbose_name='Fecha de Creacion')
    history = HistoricalRecords()
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.nombre}"

    def name(self):
        return str(f"{self.nombre}{' ' + self.descripcion if self.descripcion else ''} {self.nombre}")
    
    class Meta:
        verbose_name_plural = "Métodos de Pago"  # Puedes personalizar el nombre plural en el admin
        #ordering = ['nombre']  # Puedes especificar el orden predeterminado de los objetos en las consultas

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=10, validators=[validar_nombre], default='Identidad',verbose_name='Nombre del documento')
    status = models.CharField(max_length=2, choices=(('1', 'Activo'), ('2', 'Inactivo')), default='1', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now=True, editable=False,verbose_name='Fecha de Creacion')
    history = HistoricalRecords()
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre}"
    
    def name(self):
        return str(f"{self.nombre}")
    
    class Meta:
        verbose_name = "Tipo de Documento"
        #ordering = ['nombre']

class TipoCargo(models.Model):
    nombre = models.CharField(max_length=50, validators=[validar_nombre],null=False,verbose_name='Nombre del Cargo')
    descripcion = models.CharField(max_length=40, blank=True, null=True, validators=[validar_descripcion], verbose_name="Descripción")
    status = models.CharField(max_length=2, choices=(('1', 'Activo'), ('2', 'Inactivo')), default='1', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now=True, editable=False,verbose_name='Fecha de Creacion')
    history = HistoricalRecords()
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.nombre}"

    def name(self):
        return str(f"{self.nombre}{' ' + self.descripcion if self.descripcion else ''} {self.nombre}")
    
    class Meta:
        verbose_name = "Tipo de Cargo"
        #ordering = ['nombre']

class Clientes(models.Model):
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, default=1)
    documento = models.CharField(max_length=21, validators=[validar_id],null=False,editable=True,verbose_name='Documento')
    nombre = models.CharField(max_length=65,validators=[validar_nombre],null=False,editable=True,verbose_name='Nombre')
    apellido = models.CharField(max_length=65,validators=[validar_nombre],null=False,editable=True,verbose_name='Apellido')
    telefono = models.CharField(max_length=10, validators=[validar_telefono],null=False,editable=True,verbose_name='Telefono')
    correo = models.CharField(max_length=50, validators=[validar_correo],null=False,editable=True,verbose_name='Correo')
    direccion = models.CharField(max_length=150, validators=[validar_direccion],null=False,editable=True,verbose_name='Dirrecion')
    rtn = models.CharField(max_length=14, validators=[validar_rtn],null=True,blank=True,editable=True,verbose_name='RTN')
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False,verbose_name='Fecha de Creacion')
    history = HistoricalRecords()
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        #ordering = ['nombre','apellido','telefono','correo','direccion']

    def __str__(self):
        return f"{self.nombre}"
    
    def name(self):
        return str(f"{self.nombre}{' ' + self.apellido if self.apellido else ''} {self.nombre}")

class Categoria(models.Model):
    nombre = models.CharField(max_length=65, validators=[validar_nombre],null=False,editable=True,verbose_name='Nombre Categoria')
    descripcion = models.CharField(max_length=400, blank=True, null=True, validators=[validar_descripcion], verbose_name="Descripción")
    status = models.CharField(max_length=2, choices=(('1', 'Activo'), ('2', 'Inactivo')), default='1', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now=True, editable=False,verbose_name='Fecha de Creacion')
    history = HistoricalRecords()
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        #ordering = ['nombre']
        
    def __str__(self):
        return f"{self.id} - {self.nombre}"
    
    def name(self):
        return str(f"{self.nombre}{' ' + self.descripcion if self.descripcion else ''} {self.nombre}")

class Proveedor(models.Model):
    nombre = models.CharField(max_length=65, validators=[validar_nombre],null=False,editable=True,verbose_name='Nombre Proveedor')
    telefono = models.CharField(max_length=10, validators=[validar_telefono],null=False,editable=True,verbose_name='Telefono de Empresa')
    correo = models.CharField(max_length=50, validators=[validar_correo],null=False,editable=True,verbose_name='Correo')
    direccion = models.CharField(max_length=255, validators=[validar_direccion],null=False,editable=True,verbose_name='Direccion')
    rtn = models.CharField(max_length=14, validators=[validar_rtn],null=False,editable=True,verbose_name='RTN')
    nombre_contacto = models.CharField(max_length=50, validators=[validar_nombre],null=False,editable=True,verbose_name='Nombre de Contacto')
    telefono_contacto = models.CharField(max_length=50, validators=[validar_telefono],null=False,editable=True,verbose_name='Numero de Contacto')
    fecha_creacion = models.DateTimeField(auto_now=True, editable=False,verbose_name='Fecha de Creacion')
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        #ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre}"

    def name(self):
        return str(f"{self.nombre}{' ' + self.direccion if self.direccion else ''} {self.nombre}")
    
class Descuento(models.Model):
    nombre = models.CharField(max_length=40, unique=True, validators=[validar_nombre],null=False,editable=True,verbose_name='Nombre Descuento')
    descripcion = models.CharField(max_length=30, blank=True, null=True, validators=[validar_descripcion], verbose_name="Descripción")
    valor = models.DecimalField(max_digits=5, decimal_places=2,default=00.00, null=False, editable=True, verbose_name='Valor del Descuento')
    fecha_creacion = models.DateTimeField(auto_now=True, editable=False,verbose_name='Fecha de Creacion')
    history = HistoricalRecords()
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Descuentos"
        verbose_name = "Descuento" 
        #ordering = ['nombre','valor']
    
    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)   
    
    def __str__(self):
        return str(f"{self.valor}")    
        #{self.nombre} - 

class Impuesto(models.Model):
    nombre = models.CharField(max_length=40, validators=[validar_nombre],null=False,editable=True,verbose_name='Nombre Impuesto')
    descripcion = models.CharField(max_length=30, blank=True, null=True, validators=[validar_descripcion], verbose_name="Descripción")
    valor = models.DecimalField(max_digits=5, decimal_places=2,default=00.00, null=False, editable=True, verbose_name='Valor del Impuesto')
    fecha_creacion = models.DateTimeField(auto_now=True, editable=False,verbose_name='Fecha de Creacion')
    history = HistoricalRecords()
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.valor}"
        # {self.nombre} - 

    class Meta:
        verbose_name_plural = "Impuestos"
        verbose_name = "Impuesto" 
        #ordering = ['nombre','valor']
    
    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)
        
@receiver(pre_save, sender=Impuesto)
def impuesto_previo(sender, instance, **kwargs):
    if instance._state.adding:
        instance.fecha_creacion = timezone.now()
    
class Producto(models.Model):
    nombre = models.CharField(max_length=50, validators=[validar_nombre],null=False,editable=True,verbose_name='Nombre')
    descripcion = models.CharField(max_length=40, blank=True, null=True, validators=[validar_descripcion], verbose_name="Descripción")
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2,validators=[validar_precio],null=False,editable=True,verbose_name='Precio Venta')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,default=1, verbose_name='Categoria')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE,default=1, verbose_name='Proveedor')
    impuesto = models.ForeignKey(Impuesto, on_delete=models.CASCADE,default=1, verbose_name='Impuesto')    
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE,default=1, verbose_name='Descuento')    
    fecha_vencimiento = models.DateField(validators=[validar_fecha_vencimiento])
    status = models.CharField(max_length=2, choices=(('1', 'Activo'), ('2', 'Inactivo')), default='1', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now=True, editable=False,verbose_name='Fecha de Creacion')
    history = HistoricalRecords()
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        #ordering = ['nombre', 'categoria', 'proveedor', 'precio_venta', 'status']

    def __str__(self):
        return f"{self.nombre} - {self.categoria}"
    
    def name(self):
        return str(f"{self.nombre}{' ' + self.precio_venta if self.precio_venta else ''} {self.nombre}")
     
class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=0,validators=[validar_Cantidad],null=True, editable=True, default=0, verbose_name='Cantidad') 
    stock_maximo = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_nivel_maximo_stock],null=False,editable=True,verbose_name='Stock Maximo')
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_nivel_minimo_stock],null=False,editable=True,verbose_name='Stock Minimo')
    status = models.CharField(max_length=2, choices=(('1', 'Activo'), ('2', 'Inactivo')), default='1', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now=True, editable=False,verbose_name='Fecha de Creacion')
    history = HistoricalRecords()
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto}-{self.cantidad}"
    
    def name(self):
        return str(f"{self.producto.nombre}{' ' + self.producto.precio_venta if self.producto.precio_venta else ''} {self.producto.nombre}")
    
    class Meta:
        verbose_name = "Inventario" 
        verbose_name_plural = "Inventarios"
        #ordering = ['status', 'cantidad']
    
class Sucursal(models.Model):
    #inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=65, validators=[validar_nombre], editable=True, verbose_name="Nombre Sucursal")
    ciudad = models.CharField(max_length=65, validators=[validar_nombre], editable=True, verbose_name="Ciudad de la sucursal")
    direccion = models.CharField(max_length=255, validators=[validar_direccion], editable=True, verbose_name="Direccion de la sucursal")
    telefono = models.CharField(max_length=8, validators=[validar_telefono], editable=True, verbose_name="Telefono de la sucursal")
    rtn = models.CharField(max_length=14, validators=[validar_rtn], editable=True, verbose_name="RTN de la sucursal")
    inventarios = models.ManyToManyField(Inventario, related_name="sucursales", verbose_name="Inventarios")
    status = models.CharField(max_length=2, choices=(('1','Activo'), ('2','Inactivo')), default='1', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now=True, editable=False, verbose_name="Fecha de Creacion")
    history = HistoricalRecords()
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        #ordering = ['nombre', 'ciudad', 'status', 'fecha_creacion']
    
    def __str__(self):
        return self.nombre
    
    def name(self):
        return f"{self.id} - {self.nombre}{' ' + self.ciudad if self.direccion else ''}"
    
class Empleados(models.Model):
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, default=1)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="Usuario", null=True, blank=True, related_name='empleado')
    nombre = models.CharField(max_length=65, null=False, validators=[validar_nombre], verbose_name='Nombre')
    apellido = models.CharField(max_length=65, null=False, validators=[validar_nombre], verbose_name='Apellido')
    documento = models.CharField(unique=True, max_length=15, null=False, verbose_name='Documento')
    fecha_nacimiento = models.DateField(validators=[validar_fecha_nacimiento], null=False, verbose_name='Fecha de nacimiento')
    telefono = models.CharField(max_length=10, null=False, validators=[validar_telefono], verbose_name='Telefono')
    correo = models.CharField(max_length=50, null=False, validators=[validar_correo], verbose_name='Correo')
    direccion = models.CharField(max_length=80, null=False, validators=[validar_direccion], verbose_name="Dirección")
    status = models.BooleanField(default=True, verbose_name="Estado")
    cargo = models.ForeignKey(TipoCargo, on_delete=models.CASCADE, verbose_name='Cargo')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=1, verbose_name='Sucursal')
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Fecha de Creacion')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        #ordering = ['nombre', 'apellido', 'status', 'fecha_creacion']

    def __str__(self):
        return f"{self.id} - {self.nombre}{' ' + self.apellido if self.apellido else ''}"

    def name(self):
        return f"{self.nombre}{' ' + self.apellido if self.apellido else ''}"

class DetalleCompra(models.Model):
    producto = models.ManyToManyField(Inventario,through='Compra')
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name='Descuento')
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[validar_valor_impuesto],verbose_name='Impuesto')
    sub_total = models.DecimalField(max_digits=10, default=0, decimal_places=2, null=False, editable=True,verbose_name='Sub Total')
    total = models.DecimalField(max_digits=10, default=0, decimal_places=2, validators=[validar_Total_Cotizacion],verbose_name='Total')
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Fecha de Creacion')
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle Compra #{self.id}"

    class Meta:
        verbose_name_plural = "Detalles de Compras"
        verbose_name = "Detalle de Compra"

class Compra(models.Model):
    detalle = models.ForeignKey(DetalleCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=0,validators=[validar_Cantidad],editable=True,verbose_name='Cantidad') 
    precio_compra = models.DecimalField(max_digits=10,default=0, decimal_places=2, validators=[validar_precio],verbose_name='Pecio de Compra')
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compra #{self.id}"

    @staticmethod
    def get_decimal_value(value):
        try:
            return Decimal(str(value))
        except Exception as e:
            print(f"Error al convertir a decimal: {e}")
            return Decimal('0')

    class Meta:
        verbose_name_plural = "Compras"
        verbose_name = "Compra"

@receiver(post_save, sender=Compra)
def aumentar_inventario_postSave(sender, instance, created, **kwargs):
    if created:
        instance.producto.cantidad += instance.cantidad
        instance.producto.save()

@receiver(post_save, sender=Compra)
def campos_calculados(sender, instance, **kwargs):
    compra = instance.detalle  # Use the actual foreign key field name

    # Now you can access related objects like this:
    items = Compra.objects.filter(detalle=compra)
    sub_total = 0
    impuesto = 0
    descuento = 0
    
    for i in items:
        sub_total += abs(i.cantidad * i.precio_compra)

    for i in items:
        impuesto += abs((sub_total) * (i.producto.producto.impuesto.valor))

    for i in items:
        descuento += abs((sub_total) * (i.producto.producto.descuento.valor))
    
    compra.sub_total = sub_total
    compra.impuesto = impuesto
    compra.descuento = descuento
    compra.total = abs(((compra.sub_total) - (compra.descuento)) + (compra.impuesto))
    compra.save()
    
#Con esto de aqui se genera el numero de factura
class ParametroSar(models.Model):
    numero_inicio= models.CharField(max_length=3,editable=True,null=False,help_text="De valor puede ser 000 o el valor que se le fue asignado por el SAR",verbose_name='Punto de Establecimiento ')
    numero_fin= models.CharField(max_length=2,editable=True,null=False,help_text="De valor puede ser 01 o el valor que se le fue asignado por el SAR",verbose_name='Tipo de Documento')
    fecha_creacion = models.DateTimeField(auto_now=True,editable=False,verbose_name='Fecha Creacion')
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Parámetros de Sar"
        verbose_name_plural = "Parámetros de Sar"
        #ordering = ['-numero_inicio', 'numero_fin']

    def __str__(self):
        return f"Inicio: {self.numero_inicio} - Final: {self.numero_fin}"     

class FacturaParametro(models.Model):
    sucursal = models.ForeignKey(Sucursal,on_delete=models.CASCADE)
    parametros = models.ForeignKey(ParametroSar,on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(verbose_name='Fecha Emision', default=timezone.now, editable=False)
    fecha_limite = models.DateField(verbose_name='Fecha Límite',validators=[validar_fecha_no_pasado],null=False,editable=True)
    cai = models.CharField(max_length=32,unique=True, validators=[validar_cai],null=False,editable=True,verbose_name='Cai',help_text='Formato: XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XX')
    
    def fill_rango_inicial(self):
        return str(self.rango_inicial_factura).zfill(8)
    def fill_rango_final(self):
        return str(self.rango_final_factura).zfill(8)

    rango_inicial_factura = models.CharField(max_length=16,null=False,editable=True,verbose_name='Rango Inicial Factura',validators=[validar_rango_inicial])
    rango_final_factura = models.CharField(max_length=16,null=False,editable=True,verbose_name='Rango Final Factura',validators=[validar_rango_final])
    status = models.CharField(max_length=2, choices=(('1','Activo'), ('2','Inactivo')), default='1', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Creación")
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        self.cai = self.formato_cai()
        
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sucursal: {self.sucursal.nombre} - Parametros de Factura: {self.id}"     
    
    def clean(self):
        super().clean()

        self.rango_inicial_factura = self.fill_rango_inicial()
        self.rango_final_factura = self.fill_rango_final()

        if self.rango_inicial_factura >= self.rango_final_factura:
            raise ValidationError({'self.rango_inicial_factura': 'El rango inicial debe ser menor que el rango final'})
    
        #Validación personalizada para el rango final
        # validar_rango_final(self.rango_final_factura, self.rango_inicial_factura)
        
    def formato_cai(self):
        return f"{self.cai[:6]}-{self.cai[6:12]}-{self.cai[12:18]}-{self.cai[18:24]}-{self.cai[24:30]}-{self.cai[30:]}"
    
    #def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Parámetros de Factura"
        #ordering = ['status']
 
class FacturaDet(models.Model):
    producto = models.ManyToManyField(Inventario,through='DetalleVenta')
    sub_total = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    descuento = models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False)
    impuesto = models.DecimalField(max_digits=10,decimal_places=2,default=0, validators=[validar_valor_impuesto],editable=False)
    total = models.DecimalField(max_digits=10,default=0, decimal_places=2,editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación",editable=False)
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle de Factura: {self.id}"
    
    class Meta:
        verbose_name_plural = "Detalles Facturas"
        verbose_name = "Detalle Factura"
        #ordering = ['sub_total', 'descuento', 'impuesto', 'total', 'created_at']
               
class DetalleVenta(models.Model):
    detalle = models.ForeignKey(FacturaDet, on_delete=models.CASCADE)
    producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10,decimal_places=2,default=0, validators=[validar_Cantidad],null=True, blank=False, verbose_name='Cantidad')  
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.usuario:
            self.usuario = get_user(kwargs.get('request'))
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        errors = {}
        if self.cantidad > self.producto.cantidad:
            errors['cantidad'] = ValidationError("No se puede vender más de lo que tienes en stock.")
        if self.cantidad <= 0:
            errors['cantidad'] = ValidationError("La cantidad debe ser mayor que 0")

        if errors:
            raise ValidationError(errors)
    
    @staticmethod
    def parse_to_decimal(value):
        try:
            return Decimal(str(value))
        except Exception as e:
            print(f"Error al convertir a decimal: {e}")
            return Decimal('0')
        
    def __str__(self):
        return '{}'.format(self.detalle)
    
    class Meta:
        verbose_name_plural = "Detalles ventas"
        verbose_name = "Detalle Venta"
        unique_together = (('detalle', 'producto'),)  # Corregido aquí
        #ordering = ['-id', 'producto', 'cantidad']
        
@receiver(post_save, sender = DetalleVenta)
def campos_calculados(sender, instance, **kwargs):
    detalleVenta = instance.detalle
    items = DetalleVenta.objects.filter(detalle = detalleVenta)
    sub_total = 0
    impuesto = 0
    descuento = 0
    
    for i in items:
        sub_total += abs(i.cantidad * i.producto.producto.precio_venta)

    for i in items:
        impuesto += abs((sub_total) * (i.producto.producto.impuesto.valor))

    for i in items:
        descuento += abs((sub_total) * (i.producto.producto.descuento.valor))
    
    instance.detalle.sub_total = sub_total
    instance.detalle.impuesto = impuesto
    instance.detalle.descuento = descuento
    instance.detalle.total = abs(((instance.detalle.sub_total) - (instance.detalle.descuento)) + (instance.detalle.impuesto))
    instance.detalle.save()

@receiver(post_save, sender=DetalleVenta)
def actualizar_inventario_al_guardar(sender, instance, created, **kwargs):
    if created:
        instance.producto.cantidad = instance.producto.cantidad - instance.cantidad
        instance.producto.save()

@receiver(post_delete, sender=DetalleVenta)
def actualizar_inventario_al_borrar(sender, instance, **kwargs):
    instance.producto.cantidad = instance.producto.cantidad + instance.cantidad
    instance.producto.save()

class Factura(models.Model):
    parametros = models.ForeignKey(FacturaParametro,on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Empleado",
        null=True,
        editable=False
    )
    
    def incrementar_numero_factura(self):
        ultimaFactura = Factura.objects.filter(parametros=self.parametros).order_by('id').last()
        if self.parametros:
            if not ultimaFactura:
                return self.parametros.rango_inicial_factura
        
            numeroFactura = int(ultimaFactura.numero_factura)
            rangoFinal = int(self.parametros.rango_final_factura)
        
            if numeroFactura >= rangoFinal:
                return None
            else:
                NuevaFactura = numeroFactura + 1
                return str(NuevaFactura).zfill(8)
    
    numero_factura = models.CharField(max_length=8,editable=False,verbose_name='Consecutivo') 
    cliente = models.ForeignKey(Clientes,on_delete=models.CASCADE,verbose_name='Cliente',  help_text= 'Consumidor Final')
    tipo_pago = models.ForeignKey(MetodosPago,on_delete=models.CASCADE,verbose_name='Metodo de Pago')
    tarjeta= models.CharField(max_length=16,null=True,blank=True, validators=[validar_numero_tarjeta],verbose_name='Tarjeta')
    efectivo= models.CharField(max_length=40,null=True, blank=True,verbose_name='Efectivo')
    hora = models.DateTimeField(default=timezone.now, editable=False)
    fecha_creacion = models.DateTimeField(auto_now=True)
    detalle = models.ForeignKey(FacturaDet,on_delete=models.CASCADE,verbose_name='Detalle')
    
    def __str__(self) -> str:
        return f"Cliente: {self.cliente.nombre} {self.cliente.apellido} - N.Factura: {self.numero_factura}"
     
    def save(self, *args, **kwargs):
        # if not self.pk and not self.usuario:
        #     self.usuario = get_user(kwargs.get('request'))
        # super().save(*args, **kwargs)
    
        # Lógica para incrementar el número de factura
        numero_factura = self.incrementar_numero_factura()
        if numero_factura is None:
            print("Advertencia: Se ha alcanzado el rango final de facturación. No se generará una nueva factura.")
        else:
            self.numero_factura = numero_factura
            print(f"Nuevo número de factura: {numero_factura}")
        super().save(*args, **kwargs)
    
    def clean(self):
        super().clean()
        numero_factura = self.incrementar_numero_factura()
        if numero_factura is None:
            raise ValidationError(("Se ha alcanzado el rango final de facturación. No se generará una nueva factura."), code='rango_final_factura')
    
    class Meta:
        verbose_name_plural = "Facturas"
        verbose_name = "Factura"
        #ordering = ['-fecha_creacion', 'parametros__sucursal__nombre', 'numero_factura']

class Rutas(models.Model):
    ruta = models.CharField(max_length=50, validators=[validar_descripcion])
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Empleado")
    def save(self, *args, **kwargs):

        if not self.usuario:
            # Si el campo usuario no tiene valor, establecemos el usuario en línea actual
            user_model = get_user_model()
            self.usuario = user_model.objects.get(pk=1)  # Puedes ajustar esto según tu lógica para obtener el usuario en línea
    
    def __str__(self):
        return str(self.ruta)

    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
    
class Transporte(models.Model):
    ruta = models.ForeignKey(Rutas, on_delete=models.CASCADE,default=1)
    nombre_carro = models.CharField(max_length=50, validators=[validar_nombre])
    codigo = models.CharField(max_length=50, validators=[validar_placa_honduras])
    chofer = models.ForeignKey(Empleados, on_delete=models.CASCADE,default=1)

    def __str__(self):
        try:
            return str(self.ruta)
        except Exception as e:
            return f"Error al representar la ruta: {e}"
    
    class Meta:
        verbose_name = 'Transporte'
        
class Entrega(models.Model):
    carro = models.ForeignKey(Transporte, on_delete=models.CASCADE, default=1)
    fecha_entrega = models.DateField(null=True, blank=True, validators=[validar_fecha_no_pasado])
    hora_entrega = models.TimeField(null=True, blank=True)
    direccion_entrega = models.CharField(max_length=255, null=True, blank=True, validators=[validar_direccion])
    
    def __str__(self):
        return str(self.direccion_entrega)
    
    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'

class Devoluciones(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE,default=1)
    cantidad = models.IntegerField(validators=[validar_Cantidad])
    descripcion = models.CharField(max_length=255,validators=[validar_descripcion])
    fecha_devolucion = models.DateField(validators=[validar_date_time])
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Empleado")
    
    def save(self, *args, **kwargs):

        if not self.usuario:
            # Si el campo usuario no tiene valor, establecemos el usuario en línea actual
            user_model = get_user_model()
            self.usuario = user_model.objects.get(pk=1)  # Puedes ajustar esto según tu lógica para obtener el usuario en línea
    
    class Meta:
        verbose_name = 'Devolucion'
        verbose_name_plural = 'Devoluciones'

@receiver(post_save, sender=Devoluciones)
def aumentar_stock(sender, instance, created, **kwargs):
    if created:  # Asegurarse de que sea una nueva devolución
        producto_devuelto = instance.id_producto
        cantidad_devuelta = instance.cantidad

        inventario_producto = Inventario.objects.get(producto=producto_devuelto)
        inventario_producto.cantidad += cantidad_devuelta
        inventario_producto.save()

    class Meta:
        verbose_name = 'Devolucion'
        verbose_name_plural = 'Devoluciones'

    def __str__(self):
        return self.descripcion

class Cotizacion(models.Model):
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
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
        return str(self.id_cliente)  # Devuelve una representación de cadena del objeto Clientes

class Pedido(models.Model):
    id_clientes = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total_pedido = models.FloatField(validators=[validar_total_pedido], null=True, blank=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Empleado")
    def save(self, *args, **kwargs):

        if not self.usuario:
            # Si el campo usuario no tiene valor, establecemos el usuario en línea actual
            user_model = get_user_model()
            self.usuario = user_model.objects.get(pk=1)  # Puedes ajustar esto según tu lógica para obtener el usuario en línea
    
    def __str__(self):
        return str(self.fecha_pedido)
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'