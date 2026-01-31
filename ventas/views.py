from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models, transaction
from django.db.models import Sum, Q, Count, F
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta
import requests

from .models import TasaCambio, Factura, ItemFactura, Pago
from inventario.models import Producto
from clientes.models import Cliente


@login_required
def dashboard(request):
    """Dashboard principal con estadísticas"""
    # Estadísticas del mes actual
    mes_actual = timezone.now().month
    año_actual = timezone.now().year
    
    # Ventas del mes
    ventas_mes = Factura.objects.filter(
        fecha__month=mes_actual,
        fecha__year=año_actual,
        estado__in=['PAGADA', 'PARCIAL', 'PENDIENTE']
    )
    
    total_ventas_mes_usd = ventas_mes.aggregate(Sum('total_usd'))['total_usd__sum'] or Decimal('0.00')
    total_ventas_mes_bs = ventas_mes.aggregate(
        total_bs=Sum('total_usd') * TasaCambio.get_tasa_actual()
    )['total_bs'] or Decimal('0.00')
    
    # Deudas pendientes
    facturas_pendientes = Factura.objects.filter(estado__in=['PENDIENTE', 'PARCIAL'])
    total_deudas_usd = sum(f.saldo_pendiente_usd for f in facturas_pendientes)
    
    # Productos con stock bajo
    productos_stock_bajo = Producto.objects.filter(
        cantidad__lte=F('stock_minimo'),
        activo=True
    ).count()
    
    # Tasa de cambio actual
    tasa_actual = TasaCambio.objects.first()
    
    # Últimas facturas
    ultimas_facturas = Factura.objects.all()[:10]
    
    context = {
        'total_ventas_mes_usd': total_ventas_mes_usd,
        'total_ventas_mes_bs': total_ventas_mes_bs,
        'total_deudas_usd': total_deudas_usd,
        'total_deudas_bs': TasaCambio.usd_to_bs(total_deudas_usd),
        'productos_stock_bajo': productos_stock_bajo,
        'tasa_actual': tasa_actual,
        'ultimas_facturas': ultimas_facturas,
        'num_facturas_mes': ventas_mes.count(),
    }
    
    return render(request, 'ventas/dashboard.html', context)


@login_required
def tasa_cambio_list(request):
    """Lista de tasas de cambio"""
    tasas = TasaCambio.objects.all()[:30]
    return render(request, 'ventas/tasa_cambio_list.html', {'tasas': tasas})


@login_required
def tasa_cambio_create(request):
    """Crear tasa de cambio manualmente"""
    if request.method == 'POST':
        tasa = request.POST.get('tasa')
        try:
            tasa_decimal = Decimal(str(tasa))
            hoy = timezone.now().date()
            
            tasa_obj, created = TasaCambio.objects.update_or_create(
                fecha=hoy,
                defaults={'tasa': tasa_decimal, 'fuente': 'Manual'}
            )
            
            if created:
                messages.success(request, f'Tasa creada: 1 USD = {tasa_decimal} Bs')
            else:
                messages.success(request, f'Tasa actualizada: 1 USD = {tasa_decimal} Bs')
            
            return redirect('ventas:tasa_cambio_list')
        except Exception as e:
            messages.error(request, f'Error al crear tasa: {str(e)}')
    
    return render(request, 'ventas/tasa_cambio_create.html')



@login_required
def actualizar_tasa_bcv(request):
    """Actualizar tasa desde el BCV vía API"""
    try:
        response = requests.get('https://pydolarve.org/api/v1/dollar/page', timeout=10)
        response.raise_for_status()
        data = response.json()
        
        tasa_bcv = None
        for monitor in data.get('monitors', {}).values():
            if monitor.get('title') == 'BCV':
                tasa_bcv = monitor.get('price')
                break
        
        if tasa_bcv:
            tasa_decimal = Decimal(str(tasa_bcv))
            hoy = timezone.now().date()
            
            tasa_obj, created = TasaCambio.objects.update_or_create(
                fecha=hoy,
                defaults={'tasa': tasa_decimal, 'fuente': 'BCV - API'}
            )
            
            messages.success(request, f'Tasa actualizada desde BCV: 1 USD = {tasa_decimal} Bs')
        else:
            messages.error(request, 'No se pudo obtener la tasa del BCV')
    except Exception as e:
        messages.error(request, f'Error al actualizar tasa: {str(e)}')
    
    return redirect('ventas:tasa_cambio_list')


@login_required
def tasa_cambio_delete(request, pk):
    """Eliminar tasa de cambio"""
    tasa = get_object_or_404(TasaCambio, pk=pk)
    
    # Solo permitir eliminar tasas creadas manualmente
    if 'Manual' not in tasa.fuente:
        messages.error(request, 'Solo se pueden eliminar tasas creadas manualmente')
        return redirect('ventas:tasa_cambio_list')
    
    if request.method == 'POST':
        fecha = tasa.fecha
        tasa.delete()
        messages.success(request, f'Tasa del {fecha} eliminada correctamente')
        return redirect('ventas:tasa_cambio_list')
    
    return render(request, 'ventas/tasa_cambio_confirm_delete.html', {'tasa': tasa})



@login_required
def factura_list(request):
    """Lista de facturas con filtros"""
    facturas = Factura.objects.all()
    
    # Filtros
    estado = request.GET.get('estado')
    cliente_id = request.GET.get('cliente')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if estado:
        facturas = facturas.filter(estado=estado)
    if cliente_id:
        facturas = facturas.filter(cliente_id=cliente_id)
    if fecha_desde:
        facturas = facturas.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        facturas = facturas.filter(fecha__lte=fecha_hasta)
    
    clientes = Cliente.objects.filter(activo=True)
    
    context = {
        'facturas': facturas,
        'clientes': clientes,
        'estado_seleccionado': estado,
        'cliente_seleccionado': cliente_id,
    }
    
    return render(request, 'ventas/factura_list.html', context)


@login_required
def factura_create(request):
    """Crear nueva factura"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                cliente_id = request.POST.get('cliente')
                tipo_venta = request.POST.get('tipo_venta')
                descuento_usd = Decimal(request.POST.get('descuento_usd', '0.00'))
                
                cliente = None
                if cliente_id:
                    cliente = get_object_or_404(Cliente, id=cliente_id)
                else:
                    # Si no hay cliente, la venta debe ser de CONTADO obligatoriamente
                    if tipo_venta == 'CREDITO':
                         raise ValueError('Venta a crédito requiere asignar un cliente')
                
                # Crear factura
                factura = Factura.objects.create(
                    cliente=cliente,
                    tipo_venta=tipo_venta,
                    descuento_usd=descuento_usd,
                    vendedor=request.user
                )
                
                # Agregar items
                productos_ids = request.POST.getlist('producto_id[]')
                cantidades = request.POST.getlist('cantidad[]')
                precios = request.POST.getlist('precio[]')
                
                for i, producto_id in enumerate(productos_ids):
                    if producto_id:
                        producto = get_object_or_404(Producto, id=producto_id)
                        cantidad = Decimal(cantidades[i])
                        precio = Decimal(precios[i])
                        
                        # Verificar stock
                        if producto.cantidad < cantidad:
                            raise ValueError(f'Stock insuficiente para {producto.nombre}')
                        
                        # Crear item
                        ItemFactura.objects.create(
                            factura=factura,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario_usd=precio
                        )
                        
                        # Reducir stock
                        producto.reducir_stock(cantidad)
                
                # Calcular totales
                factura.calcular_totales()
                
                # Verificar límite de crédito
                if tipo_venta == 'CREDITO' and cliente:
                    if not cliente.puede_comprar_a_credito(factura.total_usd):
                        raise ValueError('El cliente ha excedido su límite de crédito')
                
                # Si es CONTADO, registrar el pago automáticamente
                if tipo_venta == 'CONTADO':
                    metodo_pago = request.POST.get('metodo_pago')
                    referencia = request.POST.get('referencia', '')
                    monto_usd = Decimal(request.POST.get('monto_usd', '0.00'))
                    monto_bs = Decimal(request.POST.get('monto_bs', '0.00'))
                    
                    # Convertir todo a Bs para el campo monto_recibido_bs
                    tasa = TasaCambio.get_tasa_actual()
                    monto_total_bs = (monto_usd * tasa) + monto_bs
                    
                    # Crear el pago
                    if metodo_pago and monto_total_bs > 0:
                        Pago.objects.create(
                            factura=factura,
                            metodo=metodo_pago,
                            monto_recibido_bs=monto_total_bs,
                            referencia=referencia,
                            cajero=request.user
                        )
                        # Actualizar estado de la factura
                        factura.actualizar_estado()
            
            messages.success(request, f'Factura {factura.numero} creada exitosamente')
            return redirect('ventas:factura_detail', pk=factura.pk)
            
        except Exception as e:
            messages.error(request, f'Error al crear factura: {str(e)}')
            return redirect('ventas:factura_create')
    
    # GET
    productos = Producto.objects.filter(activo=True, cantidad__gt=0)
    clientes = Cliente.objects.filter(activo=True)
    
    context = {
        'productos': productos,
        'clientes': clientes,
        'tasa_actual': TasaCambio.get_tasa_actual(),
    }
    
    return render(request, 'ventas/factura_create.html', context)


@login_required
def factura_detail(request, pk):
    """Detalle de factura"""
    factura = get_object_or_404(Factura, pk=pk)
    
    context = {
        'factura': factura,
        'items': factura.items.all(),
        'pagos': factura.pagos.all(),
        'tasa_actual': TasaCambio.get_tasa_actual(),
    }
    
    return render(request, 'ventas/factura_detail.html', context)


@login_required
def factura_pagar(request, pk):
    """Registrar pago de factura"""
    factura = get_object_or_404(Factura, pk=pk)
    
    if request.method == 'POST':
        try:
            metodo = request.POST.get('metodo')
            monto_recibido = Decimal(request.POST.get('monto_recibido'))
            referencia = request.POST.get('referencia', '')
            
            # Crear pago
            pago = Pago.objects.create(
                factura=factura,
                metodo=metodo,
                monto_recibido_bs=monto_recibido,
                referencia=referencia,
                cajero=request.user
            )
            
            messages.success(
                request,
                f'Pago registrado. Vuelto: ${pago.vuelto_usd:.2f} / Bs {pago.vuelto_bs:.2f}'
            )
            return redirect('ventas:factura_detail', pk=factura.pk)
            
        except Exception as e:
            messages.error(request, f'Error al registrar pago: {str(e)}')
    
    return render(request, 'ventas/factura_pagar.html', {
        'factura': factura,
        'tasa_actual': TasaCambio.get_tasa_actual(),
    })


@login_required
def factura_anular(request, pk):
    """Anular una factura"""
    factura = get_object_or_404(Factura, pk=pk)
    
    if request.method == 'POST':
        if factura.estado == 'ANULADA':
            messages.warning(request, 'La factura ya está anulada')
        else:
            with transaction.atomic():
                # Devolver stock
                for item in factura.items.all():
                    item.producto.aumentar_stock(item.cantidad)
                
                factura.estado = 'ANULADA'
                factura.save()
            
            messages.success(request, f'Factura {factura.numero} anulada')
        
        return redirect('ventas:factura_detail', pk=factura.pk)
    
    return render(request, 'ventas/factura_anular.html', {'factura': factura})


@login_required
def reportes(request):
    """Reportes y estadísticas"""
    # Ventas por período
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if not fecha_desde:
        fecha_desde = timezone.now().date().replace(day=1)
    if not fecha_hasta:
        fecha_hasta = timezone.now().date()
    
    facturas = Factura.objects.filter(
        fecha__date__gte=fecha_desde,
        fecha__date__lte=fecha_hasta,
        estado__in=['PAGADA', 'PARCIAL', 'PENDIENTE']
    )
    
    total_ventas_usd = facturas.aggregate(Sum('total_usd'))['total_usd__sum'] or Decimal('0.00')
    
    context = {
        'facturas': facturas,
        'total_ventas_usd': total_ventas_usd,
        'total_ventas_bs': TasaCambio.usd_to_bs(total_ventas_usd),
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    }
    
    return render(request, 'ventas/reportes.html', context)
