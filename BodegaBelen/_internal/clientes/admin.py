from django.contrib import admin
from .models import Cliente, NotaCredito


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('numero_documento', 'nombre_completo', 'telefono', 'tiene_credito', 'limite_credito_usd', 'deuda_total_usd', 'activo')
    list_filter = ('tiene_credito', 'activo', 'tipo_documento')
    search_fields = ('numero_documento', 'nombre', 'apellido', 'email', 'telefono')
    ordering = ('nombre', 'apellido')
    readonly_fields = ('created_at', 'updated_at', 'deuda_total_usd', 'credito_disponible_usd')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('tipo_documento', 'numero_documento', 'nombre', 'apellido')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'direccion')
        }),
        ('Crédito', {
            'fields': ('tiene_credito', 'limite_credito_usd', 'deuda_total_usd', 'credito_disponible_usd')
        }),
        ('Estado', {
            'fields': ('activo', 'created_at', 'updated_at')
        }),
    )
    
    def nombre_completo(self, obj):
        return obj.nombre_completo
    nombre_completo.short_description = 'Nombre Completo'
    
    def deuda_total_usd(self, obj):
        return f"${obj.deuda_total_usd:,.2f}"
    deuda_total_usd.short_description = 'Deuda Total (USD)'
    
    def credito_disponible_usd(self, obj):
        return f"${obj.credito_disponible_usd:,.2f}"
    credito_disponible_usd.short_description = 'Crédito Disponible (USD)'


@admin.register(NotaCredito)
class NotaCreditoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'monto_usd', 'concepto', 'aplicada', 'fecha', 'usuario')
    list_filter = ('aplicada', 'fecha')
    search_fields = ('cliente__nombre', 'cliente__numero_documento', 'concepto')
    readonly_fields = ('fecha',)
    ordering = ('-fecha',)
