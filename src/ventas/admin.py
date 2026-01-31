from django.contrib import admin
from .models import TasaCambio, Factura, ItemFactura, Pago


@admin.register(TasaCambio)
class TasaCambioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tasa', 'fuente', 'created_at')
    list_filter = ('fuente', 'fecha')
    ordering = ('-fecha',)
    readonly_fields = ('created_at',)


class ItemFacturaInline(admin.TabularInline):
    model = ItemFactura
    extra = 1
    readonly_fields = ('subtotal_usd', 'total_usd')


class PagoInline(admin.TabularInline):
    model = Pago
    extra = 0
    readonly_fields = ('monto_usd', 'vuelto_usd', 'fecha')


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'tipo_venta', 'total_usd', 'total_bs', 'estado', 'fecha')
    list_filter = ('estado', 'tipo_venta', 'fecha')
    search_fields = ('numero', 'cliente__nombre', 'cliente__numero_documento')
    readonly_fields = ('numero', 'subtotal_bs', 'descuento_bs', 'total_bs', 'total_pagado_usd', 'saldo_pendiente_usd', 'saldo_pendiente_bs', 'fecha', 'updated_at')
    ordering = ('-fecha',)
    inlines = [ItemFacturaInline, PagoInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero', 'cliente', 'tipo_venta', 'vendedor')
        }),
        ('Montos en USD', {
            'fields': ('subtotal_usd', 'descuento_usd', 'total_usd')
        }),
        ('Montos en Bs', {
            'fields': ('tasa_cambio', 'subtotal_bs', 'descuento_bs', 'total_bs')
        }),
        ('Pagos', {
            'fields': ('total_pagado_usd', 'saldo_pendiente_usd', 'saldo_pendiente_bs')
        }),
        ('Estado y Notas', {
            'fields': ('estado', 'notas', 'fecha', 'updated_at')
        }),
    )
    
    def total_bs(self, obj):
        return f"Bs {obj.total_bs:,.2f}"
    total_bs.short_description = 'Total Bs'


@admin.register(ItemFactura)
class ItemFacturaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'producto', 'cantidad', 'precio_unitario_usd', 'descuento_usd', 'total_usd')
    search_fields = ('factura__numero', 'producto__nombre')


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('factura', 'metodo', 'monto_bs', 'monto_usd', 'vuelto_bs', 'vuelto_usd', 'estado', 'fecha')
    list_filter = ('metodo', 'estado', 'fecha')
    search_fields = ('factura__numero', 'referencia')
    readonly_fields = ('monto_usd', 'vuelto_usd', 'fecha')
    ordering = ('-fecha',)
    
    def monto_usd(self, obj):
        return f"${obj.monto_usd:,.2f}"
    monto_usd.short_description = 'Monto USD'
    
    def vuelto_usd(self, obj):
        return f"${obj.vuelto_usd:,.2f}"
    vuelto_usd.short_description = 'Vuelto USD'
