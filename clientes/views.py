from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal

from .models import Cliente, NotaCredito


@login_required
def cliente_list(request):
    """Lista de clientes"""
    clientes = Cliente.objects.filter(activo=True)
    
    # Filtros
    busqueda = request.GET.get('q')
    con_deuda = request.GET.get('con_deuda')
    
    if busqueda:
        clientes = clientes.filter(
            Q(nombre__icontains=busqueda) | 
            Q(apellido__icontains=busqueda) |
            Q(numero_documento__icontains=busqueda)
        )
    
    # Nota: filtro de deuda requiere evaluación en Python
    if con_deuda:
        clientes = [c for c in clientes if c.deuda_total_usd > 0]
    
    return render(request, 'clientes/cliente_list.html', {'clientes': clientes})


@login_required
def cliente_detail(request, pk):
    """Detalle de cliente con historial de compras"""
    cliente = get_object_or_404(Cliente, pk=pk)
    facturas = cliente.facturas.all().order_by('-fecha')
    notas_credito = cliente.notas_credito.all().order_by('-fecha')
    
    return render(request, 'clientes/cliente_detail.html', {
        'cliente': cliente,
        'facturas': facturas,
        'notas_credito': notas_credito
    })


@login_required
def cliente_create(request):
    """Crear cliente"""
    if request.method == 'POST':
        try:
            tipo_documento = request.POST.get('tipo_documento')
            numero_documento = request.POST.get('numero_documento')
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido', '')
            telefono = request.POST.get('telefono', '')
            email = request.POST.get('email', '')
            direccion = request.POST.get('direccion', '')
            tiene_credito = request.POST.get('tiene_credito') == 'on'
            limite_credito_usd = request.POST.get('limite_credito_usd', '0.00')
            
            cliente = Cliente.objects.create(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                email=email,
                direccion=direccion,
                tiene_credito=tiene_credito,
                limite_credito_usd=Decimal(limite_credito_usd) if tiene_credito else Decimal('0.00')
            )
            
            messages.success(request, f'Cliente {cliente.nombre_completo} creado exitosamente')
            return redirect('clientes:cliente_detail', pk=cliente.pk)
            
        except Exception as e:
            messages.error(request, f'Error al crear cliente: {str(e)}')
    
    return render(request, 'clientes/cliente_form.html')


@login_required
def cliente_update(request, pk):
    """Actualizar cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        try:
            cliente.tipo_documento = request.POST.get('tipo_documento')
            cliente.numero_documento = request.POST.get('numero_documento')
            cliente.nombre = request.POST.get('nombre')
            cliente.apellido = request.POST.get('apellido', '')
            cliente.telefono = request.POST.get('telefono', '')
            cliente.email = request.POST.get('email', '')
            cliente.direccion = request.POST.get('direccion', '')
            cliente.tiene_credito = request.POST.get('tiene_credito') == 'on'
            limite_credito_usd = request.POST.get('limite_credito_usd', '0.00')
            cliente.limite_credito_usd = Decimal(limite_credito_usd) if cliente.tiene_credito else Decimal('0.00')
            cliente.save()
            
            messages.success(request, f'Cliente {cliente.nombre_completo} actualizado')
            return redirect('clientes:cliente_detail', pk=cliente.pk)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar cliente: {str(e)}')
    
    return render(request, 'clientes/cliente_form.html', {'cliente': cliente})


@login_required
def cliente_delete(request, pk):
    """Eliminar cliente (desactivar)"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente.activo = False
        cliente.save()
        messages.success(request, f'Cliente {cliente.nombre_completo} desactivado')
        return redirect('clientes:cliente_list')
    
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})


@login_required
def nota_credito_create(request, cliente_id):
    """Crear nota de crédito"""
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    if request.method == 'POST':
        try:
            monto_usd = Decimal(request.POST.get('monto_usd'))
            concepto = request.POST.get('concepto')
            
            nota = NotaCredito.objects.create(
                cliente=cliente,
                monto_usd=monto_usd,
                concepto=concepto,
                usuario=request.user
            )
            
            messages.success(request, f'Nota de crédito creada por ${monto_usd}')
            return redirect('clientes:cliente_detail', pk=cliente.pk)
            
        except Exception as e:
            messages.error(request, f'Error al crear nota de crédito: {str(e)}')
    
    return render(request, 'clientes/nota_credito_form.html', {'cliente': cliente})
