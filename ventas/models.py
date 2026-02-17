from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from inventario.models import Producto
from clientes.models import Cliente


class TasaCambio(models.Model):
    """Tasa de cambio USD a Bs según BCV"""
    tasa = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Bolívares por cada dólar'
    )
    fecha = models.DateField(auto_now_add=True, unique=True)
    fuente = models.CharField(max_length=100, default='BCV')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Tasa de Cambio'
        verbose_name_plural = 'Tasas de Cambio'
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['-fecha']),
        ]
    
    def __str__(self):
        return f"{self.fecha} - 1 USD = {self.tasa} Bs"
    
    @staticmethod
    def get_tasa_actual():
        """Retorna la tasa de cambio más reciente"""
        tasa = TasaCambio.objects.first()
        return tasa.tasa if tasa else Decimal('36.00')  # Tasa por defecto
    
    @staticmethod
    def usd_to_bs(monto_usd):
        """Convierte USD a Bs"""
        tasa = TasaCambio.get_tasa_actual()
        return Decimal(str(monto_usd)) * tasa
    
    @staticmethod
    def bs_to_usd(monto_bs):
        """Convierte Bs a USD"""
        tasa = TasaCambio.get_tasa_actual()
        return Decimal(str(monto_bs)) / tasa


class Factura(models.Model):
    """Facturas de venta"""
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Pago Parcial'),
        ('PAGADA', 'Pagada'),
        ('ANULADA', 'Anulada'),
    ]
    
    TIPO_VENTA_CHOICES = [
        ('CONTADO', 'Contado'),
        ('CREDITO', 'Crédito'),
    ]
    
    # Información básica
    numero = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='facturas', null=True, blank=True, help_text='Cliente de la venta. Si es None, es un cliente casual.')
    tipo_venta = models.CharField(max_length=10, choices=TIPO_VENTA_CHOICES, default='CONTADO')
    
    # Montos
    subtotal_usd = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    descuento_usd = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_usd = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Tasa de cambio al momento de la venta
    tasa_cambio = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Estado y control
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    
    # Auditoría
    vendedor = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Notas
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['numero']),
            models.Index(fields=['-fecha']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        cliente_nombre = self.cliente.nombre_completo if self.cliente else "Cliente Casual"
        return f"{self.numero} - {cliente_nombre}"
    
    def save(self, *args, **kwargs):
        # Generar número de factura si es nueva
        if not self.numero:
            ultimo = Factura.objects.all().order_by('-id').first()
            if ultimo:
                numero = int(ultimo.numero.split('-')[1]) + 1
            else:
                numero = 1
            self.numero = f"F-{numero:08d}"
        
        # Asignar tasa de cambio actual
        if not self.tasa_cambio:
            self.tasa_cambio = TasaCambio.get_tasa_actual()
        
        super().save(*args, **kwargs)
    
    @property
    def subtotal_bs(self):
        """Subtotal en bolívares"""
        return self.subtotal_usd * self.tasa_cambio
    
    @property
    def descuento_bs(self):
        """Descuento en bolívares"""
        return self.descuento_usd * self.tasa_cambio
    
    @property
    def total_bs(self):
        """Total en bolívares"""
        return self.total_usd * self.tasa_cambio
    
    @property
    def total_pagado_usd(self):
        """Total pagado en USD"""
        pagos = self.pagos.filter(estado='COMPLETADO')
        return sum(pago.monto_usd for pago in pagos)
    
    @property
    def saldo_pendiente_usd(self):
        """Saldo pendiente en USD"""
        return self.total_usd - self.total_pagado_usd
    
    @property
    def saldo_pendiente_bs(self):
        """Saldo pendiente en Bs"""
        return self.saldo_pendiente_usd * self.tasa_cambio
    
    def calcular_totales(self):
        """Calcula los totales de la factura"""
        items = self.items.all()
        self.subtotal_usd = sum(item.total_usd for item in items)
        self.total_usd = self.subtotal_usd - self.descuento_usd
        self.save()
    
    def actualizar_estado(self):
        """Actualiza el estado según los pagos"""
        if self.estado == 'ANULADA':
            return
        
        saldo = self.saldo_pendiente_usd
        if saldo <= Decimal('0.01'):
            self.estado = 'PAGADA'
        elif saldo < self.total_usd:
            self.estado = 'PARCIAL'
        else:
            self.estado = 'PENDIENTE'
        self.save()


class ItemFactura(models.Model):
    """Items de una factura"""
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(Decimal('0.001'))])
    precio_unitario_usd = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_usd = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    class Meta:
        verbose_name = 'Item de Factura'
        verbose_name_plural = 'Items de Factura'
    
    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
    
    @property
    def subtotal_usd(self):
        """Subtotal antes de descuento"""
        return Decimal(str(self.cantidad)) * self.precio_unitario_usd
    
    @property
    def total_usd(self):
        """Total con descuento aplicado"""
        return self.subtotal_usd - self.descuento_usd
    
    @property
    def total_bs(self):
        """Total en bolívares"""
        return self.total_usd * self.factura.tasa_cambio
    
    def save(self, *args, **kwargs):
        # Asignar precio actual del producto si es nuevo
        if not self.precio_unitario_usd:
            self.precio_unitario_usd = self.producto.precio_usd
        super().save(*args, **kwargs)


class Pago(models.Model):
    """Pagos aplicados a facturas"""
    METODO_CHOICES = [
        ('EFECTIVO_USD', 'Efectivo USD'),
        ('EFECTIVO_BS', 'Efectivo Bs'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('PUNTO_VENTA', 'Punto de Venta'),
        ('PAGO_MOVIL', 'Pago Móvil'),
        ('ZELLE', 'Zelle'),
        ('MIXTO', 'Mixto'),
        ('OTRO', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('ANULADO', 'Anulado'),
    ]
    
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='pagos')
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)
    
    # Monto recibido
    monto_recibido_bs = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Monto recibido en bolívares (o convertido a Bs si es USD)'
    )
    
    # Monto aplicado a la factura
    monto_bs = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text='Monto aplicado a la factura en Bs'
    )
    
    # Vuelto
    vuelto_bs = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Vuelto en bolívares'
    )
    
    # Tasa de cambio al momento del pago
    tasa_cambio = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Control
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='COMPLETADO')
    referencia = models.CharField(max_length=100, blank=True, help_text='Número de referencia bancaria')
    
    # Auditoría
    cajero = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Pago {self.factura.numero} - {self.metodo} - Bs {self.monto_bs}"
    
    @property
    def monto_usd(self):
        """Monto del pago en USD"""
        return self.monto_bs / self.tasa_cambio
    
    @property
    def vuelto_usd(self):
        """Vuelto en USD"""
        return self.vuelto_bs / self.tasa_cambio
    
    def save(self, *args, **kwargs):
        # Asignar tasa de cambio actual
        if not self.tasa_cambio:
            self.tasa_cambio = TasaCambio.get_tasa_actual()
        
        # Calcular vuelto si es efectivo
        if self.metodo in ['EFECTIVO_USD', 'EFECTIVO_BS']:
            pendiente_bs = self.factura.saldo_pendiente_bs
            if self.monto_recibido_bs > pendiente_bs:
                self.monto_bs = pendiente_bs
                self.vuelto_bs = self.monto_recibido_bs - pendiente_bs
            else:
                self.monto_bs = self.monto_recibido_bs
                self.vuelto_bs = Decimal('0.00')
        else:
            self.monto_bs = self.monto_recibido_bs
            self.vuelto_bs = Decimal('0.00')
        
        super().save(*args, **kwargs)
        
        # Actualizar estado de la factura
        self.factura.actualizar_estado()
