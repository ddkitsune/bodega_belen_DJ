from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import Categoria, Producto, MovimientoInventario


class ProductoResource(resources.ModelResource):
    """Recurso para importar/exportar productos"""
    categoria = fields.Field(
        column_name='categoria',
        attribute='categoria',
        widget=ForeignKeyWidget(Categoria, 'nombre')
    )
    
    class Meta:
        model = Producto
        fields = ('id', 'codigo', 'nombre', 'descripcion', 'categoria', 
                  'precio_usd', 'cantidad', 'stock_minimo', 'activo')
        export_order = ('codigo', 'nombre', 'categoria', 'precio_usd', 
                       'cantidad', 'stock_minimo', 'activo')
        import_id_fields = ('codigo',)  # Usar código como identificador único
        skip_unchanged = True
        report_skipped = True
    
    def before_import_row(self, row, **kwargs):
        """Validaciones antes de importar"""
        # Convertir activo a boolean si viene como texto
        if 'activo' in row:
            if isinstance(row['activo'], str):
                row['activo'] = row['activo'].lower() in ['true', '1', 'sí', 'si', 'yes']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'created_at')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):
    resource_class = ProductoResource
    list_display = ('codigo', 'nombre', 'categoria', 'precio_usd', 'precio_bs', 'cantidad', 'stock_bajo', 'activo')
    list_filter = ('activo', 'categoria')
    search_fields = ('codigo', 'nombre', 'descripcion')
    ordering = ('nombre',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'descripcion', 'categoria', 'imagen')
        }),
        ('Precios', {
            'fields': ('precio_usd',)
        }),
        ('Inventario', {
            'fields': ('cantidad', 'stock_minimo')
        }),
        ('Estado', {
            'fields': ('activo', 'created_at', 'updated_at')
        }),
    )
    
    def precio_bs(self, obj):
        return f"Bs {obj.precio_bs:,.2f}"
    precio_bs.short_description = 'Precio Bs'
    
    def stock_bajo(self, obj):
        return '⚠️ Sí' if obj.stock_bajo else 'No'
    stock_bajo.short_description = 'Stock Bajo'


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'cantidad_anterior', 'cantidad_nueva', 'usuario', 'fecha')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre', 'producto__codigo', 'motivo')
    readonly_fields = ('fecha',)
    ordering = ('-fecha',)
