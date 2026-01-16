# 🏪 Bodega de Belén - Sistema de Ventas

Sistema de gestión de ventas e inventario desarrollado con Django.

## ✨ Características

- 📦 **Gestión de Inventario**: Control de productos, categorías y stock
- 👥 **Gestión de Clientes**: Clientes con límite de crédito
- 💰 **Ventas**: Facturas de contado y crédito
- 💳 **Pagos**: Registro automático de pagos
- 📊 **Reportes**: Dashboard con estadísticas
- 💱 **Tasa de Cambio**: Integración con tasa BCV
- 📥📤 **Importar/Exportar**: Inventario desde/hacia Excel

## 🚀 Inicio Rápido

### Requisitos
- Python 3.11+
- pip

### Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/bodega-belen.git
cd bodega-belen

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

Abre tu navegador en: http://127.0.0.1:8000

### Inicio Rápido (Windows)

Simplemente ejecuta `INICIAR.bat`

## 🌐 Despliegue

### 🚂 Railway (Recomendado)

**Despliegue rápido en 10 minutos:**

1. **Guía Rápida**: Ver `RAILWAY_PASOS_RAPIDOS.md` - Pasos visuales con tiempos estimados
2. **Guía Completa**: Ver `DESPLIEGUE_RAILWAY.md` - Documentación detallada

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Deivyg4/bodega_belen_DJ)

### ☁️ Otras Plataformas

- **Vercel**: Ver `DESPLIEGUE_VERCEL.md`
- **Heroku**: Compatible con Procfile incluido
- **Render**: Compatible con configuración actual

## 📁 Estructura del Proyecto

```
bodega_belen/
├── bodega_belen/      # Configuración principal
├── inventario/        # App de inventario
├── ventas/            # App de ventas
├── clientes/          # App de clientes
├── templates/         # Plantillas HTML
├── static/            # Archivos estáticos
├── db.sqlite3         # Base de datos (desarrollo)
└── manage.py          # CLI de Django
```

## 🛠️ Tecnologías

- **Backend**: Django 5.2.9
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: Bootstrap 5
- **Importar/Exportar**: django-import-export, openpyxl

## 📝 Licencia

Este proyecto es privado.

## 👨‍💻 Autor

Desarrollado para Bodega de Belén
