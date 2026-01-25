from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Categoria(models.Model):
    """Categorías de productos"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Productos del inventario"""
    codigo = models.CharField(max_length=50, unique=True, help_text='Código único del producto')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    
    # Precios
    precio_usd = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Precio en dólares americanos'
    )
    
    # Stock
    cantidad = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Cantidad disponible en inventario'
    )
    stock_minimo = models.IntegerField(
        default=5,
        validators=[MinValueValidator(0)],
        help_text='Cantidad mínima de alerta'
    )
    
    # Imagen
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    # Estado
    activo = models.BooleanField(default=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def precio_bs(self):
        """Obtiene el precio en bolívares según la tasa actual"""
        from ventas.models import TasaCambio
        tasa = TasaCambio.get_tasa_actual()
        return self.precio_usd * tasa if tasa else Decimal('0.00')

    @property
    def stock_bajo(self):
        """Verifica si el stock está por debajo del mínimo"""
        return self.cantidad <= self.stock_minimo

    def reducir_stock(self, cantidad):
        """Reduce el stock del producto"""
        if self.cantidad >= cantidad:
            self.cantidad -= cantidad
            self.save()
            return True
        return False

    def aumentar_stock(self, cantidad):
        """Aumenta el stock del producto"""
        self.cantidad += cantidad
        self.save()


class MovimientoInventario(models.Model):
    """Registro de movimientos de inventario"""
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    cantidad_anterior = models.IntegerField()
    cantidad_nueva = models.IntegerField()
    motivo = models.TextField()
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} - {self.cantidad} unidades"
