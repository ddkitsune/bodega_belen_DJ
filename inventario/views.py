from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.db.models import Q, F
from .models import Producto, Categoria, MovimientoInventario


@login_required
def producto_list(request):
    """Lista de productos"""
    productos = Producto.objects.filter(activo=True).select_related('categoria')
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    stock_bajo = request.GET.get('stock_bajo')
    busqueda = request.GET.get('q')
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if stock_bajo:
        productos = productos.filter(cantidad__lte=F('stock_minimo'))
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | 
            Q(codigo__icontains=busqueda)
        )
    
    categorias = Categoria.objects.filter(activo=True)
    
    return render(request, 'inventario/producto_list.html', {
        'productos': productos,
        'categorias': categorias
    })


@login_required
def producto_detail(request, pk):
    """Detalle de producto"""
    producto = get_object_or_404(Producto, pk=pk)
    movimientos = producto.movimientos.all()[:20]
    
    return render(request, 'inventario/producto_detail.html', {
        'producto': producto,
        'movimientos': movimientos
    })


@login_required
def producto_create(request):
    """Crear producto"""
    if request.method == 'POST':
        try:
            codigo = request.POST.get('codigo')
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion', '')
            categoria_id = request.POST.get('categoria')
            precio_usd = request.POST.get('precio_usd')
            cantidad = request.POST.get('cantidad', 0)
            stock_minimo = request.POST.get('stock_minimo', 5)
            # Checkbox returns 'on' if checked, None otherwise
            es_por_peso = request.POST.get('es_por_peso') == 'on'
            
            producto = Producto.objects.create(
                codigo=codigo,
                nombre=nombre,
                descripcion=descripcion,
                categoria_id=categoria_id if categoria_id else None,
                precio_usd=precio_usd,
                cantidad=cantidad,
                stock_minimo=stock_minimo,
                es_por_peso=es_por_peso
            )
            
            messages.success(request, f'Producto {producto.nombre} creado exitosamente')
            return redirect('inventario:producto_detail', pk=producto.pk)
            
        except Exception as e:
            messages.error(request, f'Error al crear producto: {str(e)}')
    
    categorias = Categoria.objects.filter(activo=True)
    return render(request, 'inventario/producto_form.html', {'categorias': categorias})


@login_required
def producto_update(request, pk):
    """Actualizar producto"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        try:
            producto.codigo = request.POST.get('codigo')
            producto.nombre = request.POST.get('nombre')
            producto.descripcion = request.POST.get('descripcion', '')
            categoria_id = request.POST.get('categoria')
            producto.categoria_id = categoria_id if categoria_id else None
            producto.precio_usd = request.POST.get('precio_usd')
            producto.cantidad = request.POST.get('cantidad')
            producto.stock_minimo = request.POST.get('stock_minimo')
            producto.es_por_peso = request.POST.get('es_por_peso') == 'on'
            producto.save()
            
            messages.success(request, f'Producto {producto.nombre} actualizado')
            return redirect('inventario:producto_detail', pk=producto.pk)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar producto: {str(e)}')
    
    categorias = Categoria.objects.filter(activo=True)
    return render(request, 'inventario/producto_form.html', {
        'producto': producto,
        'categorias': categorias
    })


@login_required
def producto_delete(request, pk):
    """Eliminar producto (desactivar)"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        producto.activo = False
        producto.save()
        messages.success(request, f'Producto {producto.nombre} desactivado')
        return redirect('inventario:producto_list')
    
    return render(request, 'inventario/producto_confirm_delete.html', {'producto': producto})


@login_required
def categoria_list(request):
    """Lista de categorías"""
    categorias = Categoria.objects.filter(activo=True)
    return render(request, 'inventario/categoria_list.html', {'categorias': categorias})


@login_required
def categoria_create(request):
    """Crear categoría"""
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion', '')
            
            categoria = Categoria.objects.create(
                nombre=nombre,
                descripcion=descripcion
            )
            
            messages.success(request, f'Categoría {categoria.nombre} creada')
            return redirect('inventario:categoria_list')
            
        except Exception as e:
            messages.error(request, f'Error al crear categoría: {str(e)}')
    
    return render(request, 'inventario/categoria_form.html')


@login_required
def movimiento_list(request):
    """Lista de movimientos de inventario"""
    movimientos = MovimientoInventario.objects.all().select_related('producto', 'usuario')
    
    # Filtros
    producto_id = request.GET.get('producto')
    tipo = request.GET.get('tipo')
    
    if producto_id:
        movimientos = movimientos.filter(producto_id=producto_id)
    if tipo:
        movimientos = movimientos.filter(tipo=tipo)
    
    return render(request, 'inventario/movimiento_list.html', {'movimientos': movimientos})


@login_required
def movimiento_create(request):
    """Crear movimiento de inventario"""
    if request.method == 'POST':
        try:
            producto_id = request.POST.get('producto')
            tipo = request.POST.get('tipo')
            cantidad = Decimal(request.POST.get('cantidad'))
            motivo = request.POST.get('motivo')
            
            producto = get_object_or_404(Producto, id=producto_id)
            cantidad_anterior = producto.cantidad
            
            if tipo == 'ENTRADA':
                producto.aumentar_stock(cantidad)
            elif tipo == 'SALIDA':
                if not producto.reducir_stock(cantidad):
                    raise ValueError('Stock insuficiente')
            elif tipo == 'AJUSTE':
                producto.cantidad = cantidad
                producto.save()
            
            # Registrar movimiento
            MovimientoInventario.objects.create(
                producto=producto,
                tipo=tipo,
                cantidad=cantidad,
                cantidad_anterior=cantidad_anterior,
                cantidad_nueva=producto.cantidad,
                motivo=motivo,
                usuario=request.user
            )
            
            messages.success(request, f'Movimiento registrado para {producto.nombre}')
            return redirect('inventario:movimiento_list')
            
        except Exception as e:
            messages.error(request, f'Error al crear movimiento: {str(e)}')
    
    productos = Producto.objects.filter(activo=True)
    return render(request, 'inventario/movimiento_form.html', {'productos': productos})
