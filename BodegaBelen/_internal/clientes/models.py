from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Cliente(models.Model):
    """Modelo de clientes"""
    TIPO_DOCUMENTO_CHOICES = [
        ('V', 'V - Venezolano'),
        ('E', 'E - Extranjero'),
        ('J', 'J - Jurídico'),
        ('G', 'G - Gubernamental'),
    ]
    
    # Datos personales
    tipo_documento = models.CharField(max_length=1, choices=TIPO_DOCUMENTO_CHOICES, default='V')
    numero_documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200, blank=True)
    
    # Datos de contacto
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    
    # Límite de crédito
    tiene_credito = models.BooleanField(default=False, help_text='¿El cliente puede comprar a crédito?')
    limite_credito_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Límite de crédito en USD'
    )
    
    # Estado
    activo = models.BooleanField(default=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre', 'apellido']
        indexes = [
            models.Index(fields=['numero_documento']),
            models.Index(fields=['nombre']),
        ]
    
    def __str__(self):
        return f"{self.tipo_documento}-{self.numero_documento} - {self.nombre_completo}"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del cliente"""
        if self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.nombre
    
    @property
    def deuda_total_usd(self):
        """Calcula la deuda total del cliente en USD (solo facturas a CRÉDITO)"""
        from ventas.models import Factura
        facturas_pendientes = Factura.objects.filter(
            cliente=self,
            tipo_venta='CREDITO',  # Solo facturas a crédito
            estado__in=['PENDIENTE', 'PARCIAL']
        )
        total = sum(factura.saldo_pendiente_usd for factura in facturas_pendientes)
        return Decimal(str(total))
    
    @property
    def credito_disponible_usd(self):
        """Calcula el crédito disponible del cliente en USD"""
        if not self.tiene_credito:
            return Decimal('0.00')
        return self.limite_credito_usd - self.deuda_total_usd
    
    @property
    def deuda_total_bs(self):
        """Calcula la deuda total del cliente en Bs"""
        from ventas.models import TasaCambio
        tasa = TasaCambio.get_tasa_actual()
        return self.deuda_total_usd * tasa if tasa else Decimal('0.00')
    
    def puede_comprar_a_credito(self, monto_usd):
        """Verifica si el cliente puede realizar una compra a crédito"""
        if not self.tiene_credito or not self.activo:
            return False
        return self.credito_disponible_usd >= monto_usd


class NotaCredito(models.Model):
    """Notas de crédito para ajustes de deudas"""
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='notas_credito')
    monto_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    concepto = models.TextField()
    aplicada = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'Nota de Crédito'
        verbose_name_plural = 'Notas de Crédito'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"NC-{self.id} - {self.cliente.nombre_completo} - ${self.monto_usd}"
