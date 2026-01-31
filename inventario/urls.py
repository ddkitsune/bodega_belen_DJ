from django.urls import path
from . import views
from .import_export_views import exportar_inventario, importar_inventario

app_name = 'inventario'

urlpatterns = [
    # Productos
    path('', views.producto_list, name='producto_list'),
    path('productos/crear/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('productos/<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),
    
    # Categorías
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/crear/', views.categoria_create, name='categoria_create'),
    
    # Movimientos
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('movimientos/crear/', views.movimiento_create, name='movimiento_create'),
    
    # Importar/Exportar
    path('exportar/', exportar_inventario, name='exportar_inventario'),
    path('importar/', importar_inventario, name='importar_inventario'),
]
