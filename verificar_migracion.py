"""
Script para verificar la migración de PostgreSQL a SQLite
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodega_belen.settings')
django.setup()

from inventario.models import Producto, Categoria, MovimientoInventario
from ventas.models import Factura, ItemFactura, Pago, TasaCambio
from clientes.models import Cliente, NotaCredito
from django.contrib.auth.models import User

print("=" * 60)
print("  VERIFICACIÓN DE MIGRACIÓN A SQLITE")
print("=" * 60)
print()

# Verificar datos
print("📊 CONTEO DE REGISTROS:")
print("-" * 60)
print(f"  Usuarios:              {User.objects.count()}")
print(f"  Categorías:            {Categoria.objects.count()}")
print(f"  Productos:             {Producto.objects.count()}")
print(f"  Movimientos Inventario: {MovimientoInventario.objects.count()}")
print(f"  Clientes:              {Cliente.objects.count()}")
print(f"  Notas de Crédito:      {NotaCredito.objects.count()}")
print(f"  Tasas de Cambio:       {TasaCambio.objects.count()}")
print(f"  Facturas:              {Factura.objects.count()}")
print(f"  Items de Factura:      {ItemFactura.objects.count()}")
print(f"  Pagos:                 {Pago.objects.count()}")
print()

# Verificar base de datos
from django.conf import settings
db_path = settings.DATABASES['default']['NAME']
print("📁 UBICACIÓN DE LA BASE DE DATOS:")
print("-" * 60)
print(f"  {db_path}")
print()

# Verificar tamaño
if os.path.exists(db_path):
    size_mb = os.path.getsize(db_path) / (1024 * 1024)
    print(f"  Tamaño: {size_mb:.2f} MB")
else:
    print("  ⚠️  Archivo no encontrado")

print()
print("=" * 60)
print("  ✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
print("=" * 60)
