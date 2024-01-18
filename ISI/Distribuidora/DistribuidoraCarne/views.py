from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import Factura, FacturaDet, DetalleVenta
from datetime import timedelta
from .forms import *
from django.contrib import messages

def descargar_pdf_factura(request, id):
    factura_obj = get_object_or_404(Factura, id=id)

    detalles_factura = FacturaDet.objects.filter(id=factura_obj.detalle.id)
    detalles_venta = DetalleVenta.objects.filter(detalle=factura_obj.detalle)
    
    
    def calcular_importes_por_producto(detalles_venta):
        
        importes_por_producto = []
        
        for detalle in detalles_venta:
            importe_por_producto = round(detalle.producto.producto.precio_venta * detalle.cantidad, 2)
            importes_por_producto.append(importe_por_producto)
        return importes_por_producto

    # Calcular el importe total
    #importe_total = sum(detalle.producto.producto.precio_venta * detalle.cantidad for detalle in detalles_venta)
    # Calcular los importes por producto
    importes_por_producto = calcular_importes_por_producto(detalles_venta)
    importe_total = sum(importes_por_producto)
    
    # Asegúrate de que estás pasando el objeto request a get_user
    current_user = get_user(request)

    # Obtener el nombre del cliente concatenando nombre_cliente y apellido_cliente
    nombre_cliente = f"{factura_obj.cliente.nombre} {factura_obj.cliente.apellido}"

    empleado_sucursal = factura_obj.usuario.empleado.sucursal
    empleado_nombre = factura_obj.usuario.empleado
    sucursal_id = factura_obj.usuario.empleado.sucursal.id
    sucursal_id_format = str(sucursal_id).zfill(3)

    context = {
    'encabezado': {
        'importe_total':  round(importe_total, 2),
        'importes_por_producto': [round(importe, 2) for importe in importes_por_producto],
        'numero_factura': factura_obj.numero_factura,
        'cai': factura_obj.parametros.cai,
        # 'fechaPago': factura_obj.hora.date(),
        'horafactura': factura_obj.hora,
        'cliente': factura_obj.cliente,
        'numero_inicio': factura_obj.parametros.parametros.numero_inicio,
        'numero_final': factura_obj.parametros.parametros.numero_fin,
        'sucursal': sucursal_id_format,
        'sucursal_name': empleado_sucursal.nombre if empleado_sucursal else 'N/A',
        'direccion_sucursal': empleado_sucursal.direccion if empleado_sucursal else 'N/A',
        'rtn': empleado_sucursal.rtn if empleado_sucursal else 'N/A',
        'empleado': empleado_nombre,
        'parametros': factura_obj.parametros,
        'enumerate': enumerate,  # Agrega la función enumerate al contexto

    },
    'detalles_factura': detalles_factura,
    'detalles_venta': detalles_venta,
    }

    # Renderizar la plantilla con el contexto
    html_content = render_to_string('factura.html', context)

    # Crear el PDF y devolver la respuesta
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{id}.pdf"'
    pisa_status = pisa.CreatePDF(html_content, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response

# def comprasview(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            # Crear una instancia del formulario y establecer el usuario actual
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()

            # Puedes realizar otras acciones después de guardar la instancia
            messages.success(request, 'La categoría se ha creado correctamente.')
    else:
        form = CategoriaForm()

    return render(request, 'tu_template.html', {'form': form})
