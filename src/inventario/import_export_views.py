from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from tablib import Dataset
from .admin import ProductoResource
from .models import Producto


@login_required
def exportar_inventario(request):
    """Exportar inventario a Excel"""
    producto_resource = ProductoResource()
    dataset = producto_resource.export()
    
    response = HttpResponse(
        dataset.xlsx,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="inventario.xlsx"'
    return response


@login_required
def importar_inventario(request):
    """Importar inventario desde Excel"""
    if request.method == 'POST':
        try:
            archivo = request.FILES.get('archivo')
            if not archivo:
                messages.error(request, 'Debe seleccionar un archivo')
                return redirect('inventario:importar_inventario')
            
            # Validar extensión
            # Obtener extensión en minúsculas
            ext = archivo.name.split('.')[-1].lower() if '.' in archivo.name else ''
            
            # Validar extensión
            if ext not in ['xlsx', 'csv']:
                messages.error(request, 'El archivo debe ser Excel (.xlsx) o CSV')
                return redirect('inventario:importar_inventario')
            
            # Leer archivo
            dataset = Dataset()
            try:
                if ext == 'csv':
                    imported_data = dataset.load(archivo.read().decode('utf-8'), format='csv')
                else:
                    imported_data = dataset.load(archivo.read(), format='xlsx')
            except Exception as e:
                messages.error(request, f'Error al leer el archivo. Asegúrese de que sea un archivo válido. Detalle: {str(e)}')
                return redirect('inventario:importar_inventario')
            
            # Dry run primero (validar sin guardar)
            producto_resource = ProductoResource()
            result = producto_resource.import_data(dataset, dry_run=True)
            
            if result.has_errors():
                # Mostrar errores
                errores = []
                for row in result.invalid_rows:
                    errores.append(f"Fila {row.number}: {row.error}")
                
                messages.error(
                    request, 
                    f'Se encontraron {len(errores)} errores en el archivo. ' +
                    'Por favor corrija los errores e intente nuevamente.'
                )
                
                return render(request, 'inventario/importar.html', {
                    'errores': errores[:10]  # Mostrar solo los primeros 10
                })
            
            # Si no hay errores, importar de verdad
            result = producto_resource.import_data(dataset, dry_run=False)
            
            messages.success(
                request,
                f'Inventario importado exitosamente. ' +
                f'Nuevos: {result.totals["new"]}, ' +
                f'Actualizados: {result.totals["update"]}, ' +
                f'Omitidos: {result.totals["skip"]}'
            )
            return redirect('inventario:producto_list')
            
        except Exception as e:
            messages.error(request, f'Error al importar archivo: {str(e)}')
            return redirect('inventario:importar_inventario')
    
    return render(request, 'inventario/importar.html')
