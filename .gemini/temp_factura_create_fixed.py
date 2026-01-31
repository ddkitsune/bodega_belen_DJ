@login_required
def factura_create(request):
    """Crear nueva factura"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                cliente_id = request.POST.get('cliente')
                tipo_venta = request.POST.get('tipo_venta')
                descuento_usd = Decimal(request.POST.get('descuento_usd', '0.00'))
                
                cliente = get_object_or_404(Cliente, id=cliente_id)
                
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
                        cantidad = int(cantidades[i])
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
                if tipo_venta == 'CREDITO':
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
