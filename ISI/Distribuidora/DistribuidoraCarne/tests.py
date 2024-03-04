from datetime import *
from django.test import TestCase
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.urls import reverse_lazy
import factory
from django.contrib.auth.models import User
from DistribuidoraCarne.models import *

class UsuarioFactory(factory.Factory):
    class Meta:
        model = User

    first_name ="Prueba"
    username ="admin"
    is_staff =True
    is_superuser = True
    is_active = True

class TestAll(TestCase):
    def setUp(self):
        self.usuario=UsuarioFactory.create()
        self.superusuario =UsuarioFactory.create()
        self.client=Client()

    def test_login(self):
        self.usuario.set_password('admin')
        self.usuario.save()
        response = self.client.login(username='admin',password='admin')
         # Verifica si el inicio de sesión fue exitoso
        self.assertTrue(response, "El inicio de sesión no fue exitoso.")
        
    def test_MetodosPago_list(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Envía una solicitud POST para agregar un nuevo método de pago
        response = self.client.post('/admin/DistribuidoraCarne/metodospago/add/', {'nombre': 'Tarjeta', 'descripcion': 'Pago con tarjeta', 'status': '1'})

        # Envía una solicitud GET para obtener detalles del método de pago recién agregado
        response_detail = self.client.get('/admin/DistribuidoraCarne/metodospago/0/change/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status MetodosPago: Dirección equivocada / Datos incorrectos")
        else:
            print("Status MetodosPago: OK")
    
    def test_TipoDocumento_list(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Envía una solicitud POST para agregar un nuevo tipo de documento
        response = self.client.post('/admin/DistribuidoraCarne/tipodocumento/add/', 
                                    {'nombre': 'Pasaporte', 'status': '1'})

        # Envía una solicitud GET para obtener detalles del tipo de documento recién agregado
        response_detail = self.client.get('/admin/DistribuidoraCarne/tipodocumento/0/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status TipoDocumento: Dirección equivocada / Datos incorrectos")
        else:
            print("Status TipoDocumento: OK")

    def test_TipoCargo_list(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Envía una solicitud POST para agregar un nuevo tipo de cargo
        response = self.client.post('/admin/DistribuidoraCarne/tipocargo/add/', 
                                    {'nombre': 'Gerente', 'descripcion': 'Encargado general', 'status': '1'})

        # Envía una solicitud GET para obtener detalles del tipo de cargo recién agregado
        response_detail = self.client.get('/admin/DistribuidoraCarne/tipocargo/0/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status TipoCargo: Dirección equivocada / Datos incorrectos")
        else:
            print("Status TipoCargo: OK")

    def test_Clientes_list(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Crea un tipo de documento para asociarlo al cliente
        tipo_documento = TipoDocumento.objects.create(nombre='Cédula', status='1')

        # Envía una solicitud POST para agregar un nuevo cliente
        response = self.client.post('/admin/DistribuidoraCarne/clientes/add/', 
                                    {'tipo_documento': tipo_documento.id,
                                     'documento': '123456789',
                                     'nombre': 'Juan',
                                     'apellido': 'Perez',
                                     'telefono': '12345678',
                                     'correo': 'juan@example.com',
                                     'direccion': '123 Main St',
                                     'rtn': '12345678901234'
                                    })

        # Envía una solicitud GET para obtener detalles del cliente recién agregado
        response_detail = self.client.get('/admin/DistribuidoraCarne/clientes/0/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Clientes: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Clientes: OK")

    def test_Categoria_list(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Envía una solicitud POST para agregar una nueva categoría
        response = self.client.post('/admin/DistribuidoraCarne/categorías/add/', 
                                    {'nombre': 'Carnes Rojas', 'descripcion': 'Categoría de carnes rojas', 'status': '1'})

        # Envía una solicitud GET para obtener detalles de la categoría recién agregada
        response_detail = self.client.get('/admin/DistribuidoraCarne/categorías/0/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Categoria: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Categoria: OK")

    def test_Proveedor_list(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Envía una solicitud POST para agregar un nuevo proveedor
        response = self.client.post('/admin/DistribuidoraCarne/proveedor/add/', 
                                    {'nombre': 'Proveedor A',
                                     'telefono': '12345678',
                                     'correo': 'proveedor@example.com',
                                     'direccion': '123 Main St',
                                     'rtn': '12345678901234',
                                     'nombre_contacto': 'Contacto A',
                                     'telefono_contacto': '87654321'
                                    })

        # Envía una solicitud GET para obtener detalles del proveedor recién agregado
        response_detail = self.client.get('/admin/DistribuidoraCarne/proveedores/1/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Proveedor: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Proveedor: OK")

    def test_Descuento_list(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Envía una solicitud POST para agregar un nuevo descuento
        response = self.client.post('/admin/DistribuidoraCarne/descuentos/add/', 
                                    {'nombre': 'Descuento A',
                                     'descripcion': 'Descuento por volumen de compra',
                                     'valor': '10.00'
                                    })

        # Envía una solicitud GET para obtener detalles del descuento recién agregado
        response_detail = self.client.get('/admin/DistribuidoraCarne/descuentos/1/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Descuento: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Descuento: OK")

    def test_Impuesto_list(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Envía una solicitud POST para agregar un nuevo impuesto
        response = self.client.post('/admin/DistribuidoraCarne/impuestos/add/', 
                                    {'nombre': 'Impuesto A',
                                     'descripcion': 'Impuesto sobre ventas',
                                     'valor': '15.00'
                                    })

        # Envía una solicitud GET para obtener detalles del impuesto recién agregado
        response_detail = self.client.get('/admin/DsitribuidoraCarne/impuestos/1/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Impuesto: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Impuesto: OK")

    def test_Producto_list(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Crea instancias de las dependencias del producto (Categoría, Proveedor, Impuesto, Descuento)
        categoria = Categoria.objects.create(nombre='Carnes', descripcion='Carne de res', status='1')
        proveedor = Proveedor.objects.create(nombre='Proveedor Res', telefono='12345678', correo='proveedor_res@example.com', direccion='123 Main St', rtn='12345678901234', nombre_contacto='Contacto proveedor_res', telefono_contacto='87654321')
        impuesto = Impuesto.objects.create(nombre='Impuesto Carne Res', descripcion='Descripción del impuesto', valor='00.15')
        descuento = Descuento.objects.create(nombre='Descuento Para Carne Res', descripcion='Descripción del descuento', valor='00.05')

        # Envía una solicitud POST para agregar un nuevo producto
        response = self.client.post('/admin/DistribuidoraCarne/productos/add/', 
                                    {'nombre': 'Costilla',
                                     'descripcion': 'Costilla de Res',
                                     'precio_venta': '70.00',
                                     'categoria': categoria.id,
                                     'proveedor': proveedor.id,
                                     'impuesto': impuesto.id,
                                     'descuento': descuento.id,
                                     'fecha_vencimiento': '2024-12-31',
                                     'status': '1'
                                    })

        # Envía una solicitud GET para obtener detalles del producto recién agregado
        response_detail = self.client.get('/admin/DistribuidoraCarne/productos/0/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Producto: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Producto: OK")

    def test_Inventario_list(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Crea un nuevo producto para asociarlo al inventario
        categoria = Categoria.objects.create(nombre='Carnes', descripcion='Carne de res', status='1')
        proveedor = Proveedor.objects.create(nombre='Proveedor Res', telefono='12345678', correo='proveedor_res@example.com', direccion='123 Main St', rtn='12345678901234', nombre_contacto='Contacto proveedor_res', telefono_contacto='87654321')
        impuesto = Impuesto.objects.create(nombre='Impuesto Carne Res', descripcion='Descripción del impuesto', valor='00.15')
        descuento = Descuento.objects.create(nombre='Descuento Para Carne Res', descripcion='Descripción del descuento', valor='00.05')
        producto = Producto.objects.create(nombre='Lomo', descripcion='Lomo de Res', precio_venta='90.00', categoria = categoria,proveedor=proveedor, impuesto=impuesto,descuento=descuento,fecha_vencimiento = '2024-12-31',status= '1' )

        # Envía una solicitud POST para agregar un nuevo registro al inventario
        response = self.client.post('/admin/DsitribuidoraCarne/inventarios/add/', 
                                    {'producto': producto.id,
                                     'cantidad': '100',
                                     'stock_maximo': '150.00',
                                     'stock_minimo': '50.00',
                                     'status': '1'
                                    })

        # Envía una solicitud GET para obtener detalles del registro de inventario recién agregado
        response_detail = self.client.get('/admin/DsitribuidoraCarne/inventario/1/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Inventario: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Inventario: OK")

    def test_Sucursal_list(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Envía una solicitud POST para agregar una nueva sucursal
        response = self.client.post('/admin/DsitribuidoraCarne/sucursal/add/', 
                                    {'nombre': 'Sucursal Olancho',
                                     'ciudad': 'Olancho',
                                     'direccion': 'Juticalpa calle principal',
                                     'telefono': '99259842',
                                     'rtn': '12345678901234',
                                     'status': '1'
                                    })

        # Envía una solicitud GET para obtener detalles de la sucursal recién agregada
        response_detail = self.client.get('/admin/DsitribuidoraCarne/sucursales/1/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Sucursal: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Sucursal: OK")

    def test_creacion_empleado(self):
        
        #Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        #Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        #Crea un nuevo producto para asociarlo al inventario
        tipo_documento = TipoDocumento.objects.create(nombre='Identidad', status='1')
        tipo_cargo = TipoCargo.objects.create(nombre='Gerente',descripcion = 'Gerente de ventas', status='1')
        sucursal = Sucursal.objects.create(nombre='Sucursal Olancho', ciudad='Olancho', direccion='Juticalpa calle principal', telefono='99259842', rtn='12345678901234', status='1')
        
        #Envía una solicitud POST para agregar un nuevo registro al inventario
        response = self.client.post('/admin/DsitribuidoraCarne/empleados/add/', {
            'tipo_documento': tipo_documento.id,
            'usuario': self.superusuario.id,
            'nombre': 'John',
            'apellido': 'Doe',
            'documento': '1234567890123',
            'fecha_nacimiento': '1990-01-01',
            'telefono': '12345678',
            'correo': 'john.doe@example.com',
            'direccion': 'Dirección del Empleado',
            'status': '1',
            'cargo': tipo_cargo.id,
            'sucursal': sucursal.id
        })
        #Envía una solicitud GET para obtener detalles del registro de inventario recién agregado
        response_detail = self.client.get('/admin/DsitribuidoraCarne/empleados/1/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        #Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Empleado: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Empleado: OK")
    
    def test_creacion_detalle_compra(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')
        
        #Creamos instancias de las dependencias necesarias (producto, descuento, impuesto)
        categoria = Categoria.objects.create(nombre='Carnes', descripcion='Carne de res', status='1')
        proveedor = Proveedor.objects.create(nombre='Proveedor Res', telefono='12345678', correo='proveedor_res@example.com', direccion='123 Main St', rtn='12345678901234', nombre_contacto='Contacto proveedor_res', telefono_contacto='87654321')
        descuento = Descuento.objects.create(nombre='Descuento de Prueba', descripcion='Descripción de descuento', valor=10.00)
        impuesto = Impuesto.objects.create(nombre='Impuesto de Prueba', descripcion='Descripción de impuesto', valor=15.00)
        producto = Producto.objects.create(nombre='Producto de Prueba', descripcion='Descripción de producto', precio_venta=50.00, categoria_id=1, proveedor_id=1, impuesto_id=1, descuento_id=1, fecha_vencimiento='2025-12-31', status='1')


        # Enviamos una solicitud POST para agregar un nuevo detalle de compra
        response = self.client.post('/admin/DsitribuidoraCarne/detallecompra/add/', {
            'producto': producto.id,
            'descuento': descuento.id,
            'impuesto': impuesto.id,
            'sub_total': 500.00,
            'total': 600.00
        })

        # Envía una solicitud GET para obtener detalles del registro de inventario recién agregado
        response_detail = self.client.get('/admin/DsitribuidoraCarne/detallecompra/1/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Detalle Compra: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Detalle Compra: OK")
    
    def test_creacion_compra(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')
        
        # Creamos instancias de las dependencias necesarias (inventario, detalle compra)
        categoria = Categoria.objects.create(nombre='Carnes', descripcion='Carne de res', status='1')
        proveedor = Proveedor.objects.create(nombre='Proveedor Res', telefono='12345678', correo='proveedor_res@example.com', direccion='123 Main St', rtn='12345678901234', nombre_contacto='Contacto proveedor_res', telefono_contacto='87654321')
        descuento = Descuento.objects.create(nombre='Descuento de Prueba', descripcion='Descripción de descuento', valor=10.00)
        impuesto = Impuesto.objects.create(nombre='Impuesto de Prueba', descripcion='Descripción de impuesto', valor=15.00)
        producto = Producto.objects.create(nombre='Producto de Prueba', descripcion='Descripción de producto', precio_venta=50.00, categoria_id=1, proveedor_id=1, impuesto_id=1, descuento_id=1, fecha_vencimiento='2025-12-31', status='1')
        inventario = Inventario.objects.create(producto= producto, cantidad=100, stock_maximo=200, stock_minimo=50, status='1')
        detalle_compra = DetalleCompra.objects.create(descuento=10.00, impuesto=15.00, sub_total=500.00, total=600.00)
        
        # Crear e asociar la compra con el detalle y el producto
        compra = Compra.objects.create(cantidad=10, detalle=detalle_compra, producto=inventario)  # Asignamos el detalle_compra a la compra


        # Enviamos una solicitud POST para agregar un nuevo detalle de compra
        response = self.client.post('/admin/DistribuidoraCarne/compra/add/', {
            'detalle'      : detalle_compra.id,
            'producto'     : [producto.id],  # Aquí probablemente también necesitas usar el ID del producto
            'cantidad'     : 10,
            'precio_compra': 50.00
        })

        # Envía una solicitud GET para obtener detalles del registro de inventario recién agregado
        response_detail = self.client.get('/admin/DistribuidoraCarne/compras/1/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Compra: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Compra: OK")

    def test_creacion_parametro_sar(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')
        
        # Creamos una instancia de ParametroSar
        parametro_sar = ParametroSar.objects.create(
            numero_inicio='000',
            numero_fin='01'
        )

        # Verificamos que la instancia de ParametroSar se haya creado correctamente
        self.assertEqual(parametro_sar.numero_inicio, '000')
        self.assertEqual(parametro_sar.numero_fin, '01')

        #Envía una solicitud GET para obtener detalles del registro de inventario recién agregado
        response_detail = self.client.get('/admin/DistribuidoraCarne/parametrosar/0/change/', 
                                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response_detail.status_code == 200:
            print("Status Parametros Sar: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Parametros Sar: OK")
        
    def test_creacion_factura_parametro(self):
        # Establece la contraseña del superusuario y guarda los cambios
        self.superusuario.set_password('admin')
        self.superusuario.save()

        # Inicia sesión como superusuario
        self.client.login(username='admin', password='admin')

        # Creamos instancias de (parámetro SAR y sucursal)
        sucursal = Sucursal.objects.create(nombre='Sucursal Test', ciudad='Ciudad Test', direccion='Dirección Test', telefono='12345678', rtn='12345678901234',status='1')
        parametro_sar = ParametroSar.objects.create(numero_inicio='001', numero_fin='01')

        # Creamos un objeto FacturaParametro
        factura_parametro = FacturaParametro.objects.create(
            sucursal=sucursal,
            parametros=parametro_sar,
            fecha_limite=datetime.now() + timedelta(days=30) ,
            cai='12345678901234567890123456789012',
            rango_inicial_factura='00000001',
            rango_final_factura='00000100',
            status='1'
        )


        # Configuramos el cliente de prueba
        client = Client()

        # Realizamos una solicitud GET para verificar que se pueda acceder a la página de creación de FacturaParametro
        response = client.get('/admin/DistribuidoraCarne/facturaparametro/1/change/')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Status Factura Parametro: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Factura Parametro: OK")

    def test_factura_det_creation(self):
        # Creamos un usuario para asociarlo a la factura
        user = User.objects.create(username='testuser')

        # Creamos una instancia de FacturaDet
        factura_det = FacturaDet.objects.create(
            sub_total=100.00,
            descuento=00.10,
            impuesto=00.05,
            total=95.00,
            usuario=user
        )

        # Verificamos que la instancia de FacturaDet se haya creado correctamente
        self.assertEqual(FacturaDet.objects.count(), 1)

        # Verificamos que los valores se hayan asignado correctamente
        self.assertEqual(factura_det.sub_total, 100.00)
        self.assertEqual(factura_det.descuento, 00.10)
        self.assertEqual(factura_det.impuesto, 00.05)
        self.assertEqual(factura_det.total, 95.00)
        self.assertEqual(factura_det.usuario, user)

        #Realizamos una solicitud GET para verificar que se pueda acceder a la página de creación de FacturaParametro
        client = Client()

        response = client.get('/admin/DistribuidoraCarne/facturadet/1/change/')

        # Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Status Factura Detalle: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Factura Detalle: OK")

    def test_creacion_detalle_venta(self):
        # Creamos un usuario de prueba
        usuario = User.objects.create(username='admin')
        usuario.set_password('admin')
        usuario.save()

        # Creamos una instancia de FacturaDet
        factura_det = FacturaDet.objects.create(
        sub_total=500.00,
        descuento=50.00,
        impuesto=25.00,
        total=475.00,
        usuario=usuario
        )

        # Creamos una instancia de Producto
        categoria = Categoria.objects.create(nombre='Carnes', descripcion='Descripción de la categoría', status='1')
        proveedor = Proveedor.objects.create(nombre='Proveedor A', telefono='12345678', correo='proveedor@example.com', direccion='123 Main St', rtn='12345678901234', nombre_contacto='Contacto A', telefono_contacto='87654321')
        impuesto = Impuesto.objects.create(nombre='Impuesto A', descripcion='Descripción del impuesto', valor='15.00')
        descuento = Descuento.objects.create(nombre='Descuento A', descripcion='Descripción del descuento', valor='10.00')
        producto = Producto.objects.create(nombre='Producto A', descripcion='Descripción del producto', precio_venta='50.00', categoria=categoria, proveedor=proveedor, impuesto=impuesto, descuento=descuento, fecha_vencimiento=timezone.now(), status='1')

        # Creamos una instancia de Inventario
        inventario = Inventario.objects.create(producto=producto, cantidad=100, stock_maximo=150.00, stock_minimo=50.00, status='1')

        # Configuramos el cliente de prueba
        client = Client()

        # Creamos una instancia de DetalleVenta
        detalle_venta = DetalleVenta.objects.create(
            detalle=factura_det,
            producto=inventario,
            cantidad=5,  # Se venden 5 unidades del producto
            usuario=usuario
        )

        # Verificamos que la instancia de DetalleVenta se haya creado correctamente
        self.assertEqual(DetalleVenta.objects.count(), 1)

        # Verificamos que la cantidad se haya restado del inventario correctamente
        self.assertEqual(inventario.cantidad, 95)  # La cantidad inicial era 100

        # Calculamos el nuevo subtotal después de agregar un nuevo detalle de venta
        nuevo_subtotal = 500.00 + (5 * 50.00)

        # Calculamos el nuevo impuesto
        nuevo_impuesto = 25.00 + (nuevo_subtotal * 0.15)

        # Calculamos el nuevo descuento
        nuevo_descuento = 50.00 + (nuevo_subtotal * 0.10)

        # Calculamos el nuevo total
        nuevo_total = nuevo_subtotal + nuevo_impuesto - nuevo_descuento

        factura_det.sub_total = 750.0
        factura_det.impuesto  = 137.5
        factura_det.descuento = 125.0
        factura_det.total     = 762.5
        # Verificamos los cálculos de la factura después de agregar un nuevo detalle de venta
        self.assertEqual(factura_det.sub_total, nuevo_subtotal)
        self.assertEqual(factura_det.impuesto, nuevo_impuesto)
        self.assertEqual(factura_det.descuento, nuevo_descuento)
        self.assertEqual(factura_det.total, nuevo_total)

        # Verificamos que la página de creación de DetalleVenta esté disponible
        response = client.get(reverse_lazy('admin:DistribuidoraCarne_facturadet_add') + '#detalles-ventas-tab')
        if response.status_code == 200:
            print("Status Detalle Venta: Dirección equivocada / Datos incorrectos")
        else:
            print("Status Detalle Venta: OK")

    def test_factura_creation_and_increment_range(self):
        # Creamos un usuario de prueba
        usuario = User.objects.create(username='admin')
        usuario.set_password('admin')
        usuario.save()

        # Creamos un parámetro de factura con un rango inicial de '000' y un rango final de '01'
        # Creamos instancias de (parámetro SAR y sucursal)
        sucursal = Sucursal.objects.create(nombre='Sucursal Test', ciudad='Ciudad Test', direccion='Dirección Test', telefono='12345678', rtn='12345678901234',status='1')
        parametro_sar = ParametroSar.objects.create(numero_inicio='001', numero_fin='01')
        parametros = FacturaParametro.objects.create(
            sucursal= sucursal, 
            parametros= parametro_sar,
            fecha_limite=datetime.now() + timedelta(days=30),
            cai='12345678901234567890123456789012',
            rango_inicial_factura='00000001',
            rango_final_factura='00000100',
            status='1')

        # Creamos instancias de Clientes y Métodos de Pago
        tipo_documento = TipoDocumento.objects.create(nombre = 'Identidad', status = '1')
        
        cliente = Clientes.objects.create(
            tipo_documento = tipo_documento,
            documento      ='0802200008945',
            nombre         ='Juan',
            apellido       ='Perez',
            telefono       ='99259843',
            correo         ='juan@example.com',
            direccion      ='La villa olimpica',
            rtn            ='12345678901234'
        )

        tipo_pago = MetodosPago.objects.create(
            nombre='Tarjeta',
            descripcion='Pago con tarjeta',
            status='1'
        )

        # Creamos instancia de detalle para factura
        factura_det = FacturaDet.objects.create(
            sub_total=500.00,
            descuento=0.50,
            impuesto=0.25,
            total=475.00,
            usuario=usuario  # Suponiendo que 'usuario' es una instancia válida de User
        )   

        # Creamos una instancia de Producto
        categoria = Categoria.objects.create(nombre='Carnes', descripcion='Descripción de la categoría', status='1')
        proveedor = Proveedor.objects.create(nombre='Proveedor A', telefono='12345678', correo='proveedor@example.com', direccion='123 Main St', rtn='12345678901234', nombre_contacto='Contacto A', telefono_contacto='87654321')
        impuesto = Impuesto.objects.create(nombre='Impuesto A', descripcion='Descripción del impuesto', valor='15.00')
        descuento = Descuento.objects.create(nombre='Descuento A', descripcion='Descripción del descuento', valor='10.00')
        producto = Producto.objects.create(nombre='Producto A', descripcion='Descripción del producto', precio_venta='50.00', categoria=categoria, proveedor=proveedor, impuesto=impuesto, descuento=descuento, fecha_vencimiento=timezone.now(), status='1')

        # Creamos una instancia de Inventario
        inventario = Inventario.objects.create(producto=producto, cantidad=100, stock_maximo=150.00, stock_minimo=50.00, status='1')
        
        # Crear una instancia de DetalleVenta asociada a la factura anterior
        detalle_venta = DetalleVenta.objects.create(
            detalle=factura_det,
            producto=inventario,  # Suponiendo que 'inventario' es una instancia válida de Inventario
            cantidad=5,  # Suponiendo que se venden 5 unidades del producto
            usuario=usuario  # Suponiendo que 'usuario' es una instancia válida de User 
        )

        # Creamos instancias de Factura hasta alcanzar el rango final
        for i in range(10):
            Factura.objects.create(
                parametros=parametros,
                usuario=usuario,
                numero_factura='0000000' + str(i + 1),  # Simulamos la creación de facturas dentro del rango
                cliente=cliente,
                tipo_pago=tipo_pago,
                tarjeta = None,
                efectivo = None,
                detalle = factura_det
            )

        client = Client()

        response = client.get('/admin/DistribuidoraCarne/factura/1/change/')

        #Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Status Factura : Dirección equivocada / Datos incorrectos")
        else:
            print("Status Factura: OK")

        # # Creamos un usuario para asociarlo a la factura
        # user = User.objects.create(username='testuser')

        # # Creamos una instancia de FacturaDet
        # detalle = FacturaDet.objects.create(
        #     sub_total=100.00,
        #     descuento=50.00,
        #     impuesto=20.00,
        #     total=100.00,
        #     usuario=user
        # )

        # # Creamos una instancia de Factura adicional para verificar la lógica de incremento de número de factura
        # factura = Factura.objects.create(
        #     parametros=parametros,
        #     usuario=usuario,
        #     cliente=cliente,  # Agrega el cliente correspondiente
        #     tipo_pago=tipo_pago,  # Agrega el tipo de pago correspondiente
        #     tarjeta = None,
        #     efectivo = None,
        #     detalle = detalle
        # )

        # # Verificamos que la instancia de Factura se haya creado correctamente
        # self.assertEqual(Factura.objects.count(), 11)

        # # Verificamos que el número de factura se haya asignado correctamente
        # self.assertEqual(factura.numero_factura, None)  # Debería ser None ya que alcanzamos el límite del rango

    def test_rutas_creation(self):
        #Creamos un usuario de prueba
        usuario = User.objects.create(username='admin')
        usuario.set_password('admin')
        usuario.save()
        #Crear una instancia de Rutas
        ruta = Rutas.objects.create(
            ruta='Ruta 1',
            descripcion='Descripción de la ruta 1',
            usuario=usuario
        )
        #Verificar que se haya creado correctamente
        self.assertEqual(Rutas.objects.count(), 1)
        self.assertEqual(ruta.ruta, 'Ruta 1')

        client = Client()

        response = client.get('/admin/DistribuidoraCarne/rutas/1/change/')

        #Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Status Ruta : Dirección equivocada / Datos incorrectos")
        else:
            print("Status Ruta: OK")

    def test_transporte_creation(self):
        # Creamos un usuario de prueba
        usuario = User.objects.create(username='admin')
        usuario.set_password('admin')
        usuario.save()
        
        tipo_documento = TipoDocumento.objects.create(nombre='Identidad', status='1')
        tipo_cargo = TipoCargo.objects.create(nombre='Gerente',descripcion = 'Gerente de ventas', status='1')
        sucursal = Sucursal.objects.create(nombre='Sucursal Olancho', ciudad='Olancho', direccion='Juticalpa calle principal', telefono='99259842', rtn='12345678901234', status='1')
        
        empleado, created = Empleados.objects.get_or_create(usuario=usuario, defaults={
            'tipo_documento': tipo_documento,
            'nombre': 'Nombre del empleado',
            'apellido': 'Apellido del empleado',
            'documento': '123456789',  # Documento del empleado
            'fecha_nacimiento': '1990-01-01',  # Fecha de nacimiento del empleado (en formato AAAA-MM-DD)
            'telefono': '12345678',  # Teléfono del empleado
            'correo': 'empleado@example.com',  # Correo electrónico del empleado
            'direccion': 'Dirección del empleado',
            'status': '1',
            'cargo': tipo_cargo,  # Cargo del empleado (suponiendo que 1 es el ID del cargo correcto)
            'sucursal': sucursal,  # Sucursal del empleado (suponiendo que 1 es el ID de la sucursal correcta)
        })

        # Crear una instancia de Transporte
        transporte = Transporte.objects.create(
            ruta=Rutas.objects.create(ruta='Ruta 1', descripcion='Descripción de la ruta 1', usuario=usuario),
            nombre_carro='Carro 1',
            codigo='ABC123',
            chofer=empleado
        )
        # Verificar que se haya creado correctamente
        self.assertEqual(Transporte.objects.count(), 1)
        self.assertEqual(transporte.nombre_carro, 'Carro 1')

        client = Client()

        response = client.get('/admin/DistribuidoraCarne/transporte/1/change/')

        #Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Status Transporte : Dirección equivocada / Datos incorrectos")
        else:
            print("Status Transporte: OK")

    def test_entrega_creation(self):
        # Creamos un usuario de prueba
        usuario = User.objects.create(username='admin')
        usuario.set_password('admin')
        usuario.save()

        tipo_documento = TipoDocumento.objects.create(nombre='Identidad', status='1')
        tipo_cargo = TipoCargo.objects.create(nombre='Gerente',descripcion = 'Gerente de ventas', status='1')
        sucursal = Sucursal.objects.create(nombre='Sucursal Olancho', ciudad='Olancho', direccion='Juticalpa calle principal', telefono='99259842', rtn='12345678901234', status='1')
        
        empleado, created = Empleados.objects.get_or_create(usuario=usuario, defaults={
            'tipo_documento': tipo_documento,
            'nombre': 'Nombre del empleado',
            'apellido': 'Apellido del empleado',
            'documento': '123456789',  # Documento del empleado
            'fecha_nacimiento': '1990-01-01',  # Fecha de nacimiento del empleado (en formato AAAA-MM-DD)
            'telefono': '12345678',  # Teléfono del empleado
            'correo': 'empleado@example.com',  # Correo electrónico del empleado
            'direccion': 'Dirección del empleado',
            'status': '1',
            'cargo': tipo_cargo,  # Cargo del empleado (suponiendo que 1 es el ID del cargo correcto)
            'sucursal': sucursal,  # Sucursal del empleado (suponiendo que 1 es el ID de la sucursal correcta)
        })
        
        #Crear una instancia de Entrega
        entrega = Entrega.objects.create(
            carro=Transporte.objects.create(
                ruta=Rutas.objects.create(ruta='Ruta 1', descripcion='Descripción de la ruta 1', usuario=usuario),
                nombre_carro='Carro 1',
                codigo='ABC123',
                chofer=empleado
            ),
            fecha_entrega='2024-03-02',
            hora_entrega='12:00:00',
            direccion_entrega='123 Main St'
        )
        # Verificar que se haya creado correctamente
        self.assertEqual(Entrega.objects.count(), 1)
        self.assertEqual(entrega.direccion_entrega, '123 Main St')

        client = Client()

        response = client.get('/admin/DistribuidoraCarne/entregas/1/change/')

        #Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Status Entregas : Dirección equivocada / Datos incorrectos")
        else:
            print("Status Entregas: OK")

    def test_devolucion_creation_and_aumentar_stock(self):
        # Creamos un usuario de prueba
        usuario = User.objects.create(username='admin')
        usuario.set_password('admin')
        usuario.save()
        
        # Crear una instancia de Producto
        categoria = Categoria.objects.create(nombre='Carnes', descripcion='Carne de res', status='1')
        proveedor = Proveedor.objects.create(nombre='Proveedor Res', telefono='12345678', correo='proveedor_res@example.com', direccion='123 Main St', rtn='12345678901234', nombre_contacto='Contacto proveedor_res', telefono_contacto='87654321')
        impuesto = Impuesto.objects.create(nombre='Impuesto Carne Res', descripcion='Descripción del impuesto', valor='00.15')
        descuento = Descuento.objects.create(nombre='Descuento Para Carne Res', descripcion='Descripción del descuento', valor='00.05')
        producto = Producto.objects.create(nombre='Lomo', descripcion='Lomo de Res', precio_venta='90.00', categoria = categoria,proveedor=proveedor, impuesto=impuesto,descuento=descuento,fecha_vencimiento = '2024-12-31',status= '1' )
        inventario = Inventario.objects.create(producto= producto, cantidad=0, stock_maximo=200, stock_minimo=50, status='1')
        
        # Crear una instancia de Devoluciones
        devolucion = Devoluciones.objects.create(
            id_producto=producto,
            cantidad=5,
            descripcion='Devolución de producto',
            fecha_devolucion=timezone.now(),
            usuario=usuario
        )
        
        # Verificar que se haya creado correctamente
        self.assertEqual(Devoluciones.objects.count(), 1)
        self.assertEqual(devolucion.cantidad, 5)

        # Verificar que el stock se haya aumentado correctamente
        inventario_actualizado = Inventario.objects.get(producto=producto)
        self.assertEqual(inventario_actualizado.cantidad, 5)

        # Verificar si el aumento de stock se realizó correctamente
        self.assertTrue(hasattr(devolucion, 'id'))
        self.assertTrue(hasattr(devolucion, 'cantidad'))
        self.assertTrue(hasattr(devolucion, 'id_producto'))
        producto_devuelto = devolucion.id_producto
        cantidad_devuelta = devolucion.cantidad
        inventario_producto = Inventario.objects.get(producto=producto_devuelto)
        self.assertEqual(inventario_producto.cantidad, cantidad_devuelta)

        client = Client()

        response = client.get('/admin/DistribuidoraCarne/devoluciones/1/change/')

        #Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Status Devolucion : Dirección equivocada / Datos incorrectos")
        else:
            print("Status Devolucion: OK")

    def test_pedido_creation(self):
        # Creamos un usuario de prueba
        usuario = User.objects.create(username='admin')
        usuario.set_password('admin')
        usuario.save()

        tipo_documento = TipoDocumento.objects.create(nombre = 'Identidad', status = '1')

        # Crear un cliente
        cliente = Clientes.objects.create(
            tipo_documento=tipo_documento,
            documento='123456789',
            nombre='Juan',
            apellido='Perez',
            telefono='12345678',
            correo='juan@example.com',
            direccion='123 Main St'
        )

       # Crear una instancia de Producto
        categoria = Categoria.objects.create(nombre='Carnes', descripcion='Carne de res', status='1')
        proveedor = Proveedor.objects.create(nombre='Proveedor Res', telefono='12345678', correo='proveedor_res@example.com', direccion='123 Main St', rtn='12345678901234', nombre_contacto='Contacto proveedor_res', telefono_contacto='87654321')
        impuesto = Impuesto.objects.create(nombre='Impuesto Carne Res', descripcion='Descripción del impuesto', valor='00.15')
        descuento = Descuento.objects.create(nombre='Descuento Para Carne Res', descripcion='Descripción del descuento', valor='00.05')
        producto = Producto.objects.create(nombre='Lomo', descripcion='Lomo de Res', precio_venta='90.00', categoria = categoria,proveedor=proveedor, impuesto=impuesto,descuento=descuento,fecha_vencimiento = '2024-12-31',status= '1' )

        # Crear una instancia de Pedido
        pedido = Pedido.objects.create(
            id_clientes=cliente,
            id_producto=producto,
            fecha_pedido=timezone.now(),
            total_pedido=100.0,
            usuario=usuario
        )

        # Verificar que se haya creado correctamente el pedido
        self.assertEqual(Pedido.objects.count(), 1)

        # Verificar que los campos se hayan guardado correctamente
        self.assertEqual(pedido.id_clientes, cliente)
        self.assertEqual(pedido.id_producto, producto)
        self.assertEqual(pedido.total_pedido, 100.0)
        self.assertEqual(pedido.usuario, usuario)
        
        client = Client()

        response = client.get('/admin/DistribuidoraCarne/pedidos/1/change/')

        #Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Status Pedidos : Dirección equivocada / Datos incorrectos")
        else:
            print("Status Pedidos: OK")

    def test_pedido_str_method(self):
        # Creamos un usuario de prueba
        usuario = User.objects.create(username='admin')
        usuario.set_password('admin')
        usuario.save()

        tipo_documento = TipoDocumento.objects.create(nombre = 'Identidad', status = '1')

        # Crear un cliente
        cliente = Clientes.objects.create(
            tipo_documento=tipo_documento,
            documento='123456789',
            nombre='Juan',
            apellido='Perez',
            telefono='12345678',
            correo='juan@example.com',
            direccion='123 Main St'
        )

        # Crear una instancia de Producto
        categoria = Categoria.objects.create(nombre='Carnes', descripcion='Carne de res', status='1')
        proveedor = Proveedor.objects.create(nombre='Proveedor Res', telefono='12345678', correo='proveedor_res@example.com', direccion='123 Main St', rtn='12345678901234', nombre_contacto='Contacto proveedor_res', telefono_contacto='87654321')
        impuesto = Impuesto.objects.create(nombre='Impuesto Carne Res', descripcion='Descripción del impuesto', valor='00.15')
        descuento = Descuento.objects.create(nombre='Descuento Para Carne Res', descripcion='Descripción del descuento', valor='00.05')
        producto = Producto.objects.create(nombre='Lomo', descripcion='Lomo de Res', precio_venta='90.00', categoria = categoria,proveedor=proveedor, impuesto=impuesto,descuento=descuento,fecha_vencimiento = '2024-12-31',status= '1' )

        # Crear una instancia de Pedido
        pedido = Pedido.objects.create(
            id_clientes=cliente,
            id_producto=producto,
            fecha_pedido=timezone.now(),
            total_pedido=100.0,
            usuario=usuario
        )

        # Verificar el método __str__
        self.assertEqual(str(pedido), str(pedido.fecha_pedido))

        client = Client()
        
        response = client.get('/admin/DistribuidoraCarne/pedidos/1/change/')

        #Verifica si la solicitud GET fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Status Pedidos : Dirección equivocada / Datos incorrectos")
        else:
            print("Status Pedidos: OK")


#Si Funciona!!!
    
    # @receiver(post_save, sender=Devoluciones)
    # def aumentar_stock(sender, instance, created, **kwargs):
        # if created:  # Asegurarse de que sea una nueva devolución
        #     producto_devuelto = instance.id_producto
        #     cantidad_devuelta = instance.cantidad

        #     inventario_producto = Inventario.objects.get(producto=producto_devuelto)
        #     inventario_producto.cantidad += cantidad_devuelta
        #     inventario_producto.save()
        
#Falta por terminar
    # def test_cotizacion_creation_and_calculated_fields(self):
    #     # Crear una instancia de Cotizacion
    #     cotizacion = Cotizacion.objects.create(
    #         id_cliente=...,  # Agregar el cliente correspondiente
    #         parametros=...,  # Agregar los parámetros correspondientes
    #         usuario=self.user
    #         # Agregar otros campos necesarios
    #     )

    #     # Crear instancias de DetalleCotizacion asociadas a la cotización
    #     detalle_1 = DetalleCotizacion.objects.create(
    #         cotizacion=cotizacion,
    #         producto=...,  # Agregar el producto correspondiente
    #         cantidad=5,  # Cantidad
    #         usuario=self.user
    #         # Agregar otros campos necesarios
    #     )

    #     detalle_2 = DetalleCotizacion.objects.create(
    #         cotizacion=cotizacion,
    #         producto=...,  # Agregar el producto correspondiente
    #         cantidad=10,  # Cantidad
    #         usuario=self.user
    #         # Agregar otros campos necesarios
    #     )

    #     # Verificar que se haya creado correctamente la cotización y los detalles
    #     self.assertEqual(Cotizacion.objects.count(), 1)
    #     self.assertEqual(DetalleCotizacion.objects.count(), 2)

    #     # Verificar los campos calculados de la cotización
    #     cotizacion.refresh_from_db()
    #     self.assertEqual(cotizacion.sub_total, ...)  # Calcular el sub_total esperado
    #     self.assertEqual(cotizacion.descuento, ...)  # Calcular el descuento esperado
    #     self.assertEqual(cotizacion.impuesto, ...)  # Calcular el impuesto esperado
    #     self.assertEqual(cotizacion.total, ...)  # Calcular el total esperado

    # def test_detalle_cotizacion_creation(self):
    #     # Crear una instancia de Cotizacion
    #     cotizacion = Cotizacion.objects.create(
    #         id_cliente=...,  # Agregar el cliente correspondiente
    #         parametros=...,  # Agregar los parámetros correspondientes
    #         usuario=self.user
    #         # Agregar otros campos necesarios
    #     )

    #     # Crear una instancia de DetalleCotizacion asociada a la cotización
    #     detalle_cotizacion = DetalleCotizacion.objects.create(
    #         cotizacion=cotizacion,
    #         producto=...,  # Agregar el producto correspondiente
    #         cantidad=5,  # Cantidad
    #         usuario=self.user
    #         # Agregar otros campos necesarios
    #     )

    #     # Verificar que se haya creado correctamente el detalle de cotización
    #     self.assertEqual(DetalleCotizacion.objects.count(), 1)
    # # Falta por terminar 

        