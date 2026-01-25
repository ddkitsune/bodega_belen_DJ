from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Tasa de Cambio
    path('tasa-cambio/', views.tasa_cambio_list, name='tasa_cambio_list'),
    path('tasa-cambio/crear/', views.tasa_cambio_create, name='tasa_cambio_create'),
    path('tasa-cambio/actualizar/', views.actualizar_tasa_bcv, name='actualizar_tasa_bcv'),
    path('tasa-cambio/<int:pk>/eliminar/', views.tasa_cambio_delete, name='tasa_cambio_delete'),
    
    # Facturas
    path('facturas/', views.factura_list, name='factura_list'),
    path('facturas/crear/', views.factura_create, name='factura_create'),
    path('facturas/<int:pk>/', views.factura_detail, name='factura_detail'),
    path('facturas/<int:pk>/pagar/', views.factura_pagar, name='factura_pagar'),
    path('facturas/<int:pk>/anular/', views.factura_anular, name='factura_anular'),
    
    # Reportes
    path('reportes/', views.reportes, name='reportes'),
]
